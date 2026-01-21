from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number_and_name_is_valid(self):
        form_data = {
            "username": "New_Driver",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "AAA55555"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword123"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "Tesla")

    def test_manufacturer_search_by_partial_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Tes"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_manufacturer_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "Tesla")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword123"
        )
        self.client.force_login(self.user)
        self.driver1 = get_user_model().objects.create_user(
            username="Driver1",
            password="TestPassword123",
            first_name="Test",
            last_name="Driver1",
            license_number="AAA11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="Driver2",
            password="TestPassword123",
            first_name="Test",
            last_name="Driver2",
            license_number="AAA22222"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="Driver3",
            password="TestPassword123",
            first_name="Test",
            last_name="Driver3",
            license_number="AAA33333"
        )

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=Driver1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Driver1")
        self.assertNotContains(response, "Driver2")
        self.assertNotContains(response, "Driver3")

    def test_driver_search_by_partial_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=ver2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Driver2")
        self.assertNotContains(response, "Driver1")
        self.assertNotContains(response, "Driver3")

    def test_driver_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=Driver4"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Driver1")
        self.assertNotContains(response, "Driver2")
        self.assertNotContains(response, "Driver3")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword123"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="F150",
            manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer3
        )

    def test_car_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Camry")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "F150")
        self.assertNotContains(response, "Model S")

    def test_car_search_by_partial_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=F1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "F150")
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Model S")

    def test_car_search_no_results(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "F150")
        self.assertNotContains(response, "Model S")
