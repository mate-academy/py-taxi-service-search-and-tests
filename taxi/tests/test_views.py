from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm, ManufacturerSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car, Driver


class IndexViewTests(TestCase):
    def test_index_view_context(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )
        self.driver = Driver.objects.create(
            username="testdriver",
            password="testpassword",
            license_number="QWE12345",
        )

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_visits"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)


class ManufacturersViewsTests(TestCase):
    def setUp(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(name="Toyota"),
            Manufacturer(name="Ford"),
            Manufacturer(name="Chevrolet"),
        ])
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")

    def test_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_get_context_data(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm
        )

    def test_get_queryset_without_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_form_initial_data(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Ford"
        )
        search_form = response.context["search_form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(search_form.initial["name"], "Ford")

    def test_get_queryset_with_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Ford"
        )
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(manufacturer_list), 1)


class DriverViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="QWE12345",
        )
        self.client.login(username="testuser", password="testpassword")

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="password1",
            license_number="QWE12346",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="password2",
            license_number="QWE12347",
        )
        self.driver3 = get_user_model().objects.create_user(
            username="driver3",
            password="password3",
            license_number="QWE12348",
        )

    def test_get_context_data(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm
        )

    def test_get_queryset_without_search(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_search_form_initial_data(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver"
        )
        search_form = response.context["search_form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(search_form.initial["username"], "driver")

    def test_get_queryset_with_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver"
        )
        driver_list = response.context["driver_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(driver_list), 3)
        self.assertIn(self.driver1, driver_list)
        self.assertIn(self.driver2, driver_list)
        self.assertIn(self.driver3, driver_list)


class CarsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="QWE12345"
        )
        self.client.login(username="testuser", password="testpassword")

        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Prius",
            manufacturer=self.manufacturer
        )

    def test_get_context_data(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_get_queryset_without_search(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_search_form_initial_data(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        search_form = response.context["search_form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(search_form.initial["model"], "Corolla")

    def test_get_queryset_with_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        car_list = response.context["car_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(car_list), 1)
