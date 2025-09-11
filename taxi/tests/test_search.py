from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from taxi.models import Manufacturer, Car


class SearchFormsTests(TestCase):
    def test_driver_search_form_empty(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_search_form_with_data(self):
        form = DriverSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_car_search_form_empty(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_search_form_with_data(self):
        form = CarSearchForm(data={"model": "Corolla"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Corolla")

    def test_manufacturer_search_form_empty(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_search_form_with_data(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")


class SearchIntegrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="StrongPass123!",
            license_number="LIC12345",
        )
        self.client.login(username="admin", password="StrongPass123!")

        self.driver1 = get_user_model().objects.create_user(
            username="driver_one", license_number="DRI12345",
            password="StrongPass123!"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver_two", license_number="DRI54321",
            password="StrongPass123!"
        )

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                         country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda",
                                                         country="Japan")

        self.car1 = Car.objects.create(model="Corolla",
                                       manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Civic",
                                       manufacturer=self.manufacturer2)

    def test_driver_list_search(self):
        url = reverse("taxi:driver-list") + "?username=driver_one"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")

    def test_car_list_search(self):
        url = reverse("taxi:car-list") + "?model=Corolla"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Civic")

    def test_manufacturer_list_search(self):
        url = reverse("taxi:manufacturer-list") + "?name=Toyota"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")

    def test_empty_queries_return_all_objects(self):
        manufacturer_form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(manufacturer_form.is_valid())
        self.assertEqual(Manufacturer.objects.count(), 2)

        car_form = CarSearchForm(data={"model": ""})
        self.assertTrue(car_form.is_valid())
        self.assertEqual(Car.objects.count(), 2)

        driver_form = DriverSearchForm(data={"username": ""})
        self.assertTrue(driver_form.is_valid())
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_case_insensitive_matching(self):

        manufacturer_queryset = Manufacturer.objects.filter(
            name__icontains="toyota")
        self.assertIn(self.manufacturer1, manufacturer_queryset)
        self.assertNotIn(self.manufacturer2, manufacturer_queryset)

        car_queryset = Car.objects.filter(model__icontains="corolla")
        self.assertIn(self.car1, car_queryset)
        self.assertNotIn(self.car2, car_queryset)

        driver_queryset = get_user_model().objects.filter(
            username__icontains="driver_one")
        self.assertIn(self.driver1, driver_queryset)
        self.assertNotIn(self.driver2, driver_queryset)
