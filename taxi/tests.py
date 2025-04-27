from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="Test",
            last_name="Driver",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            f"{self.car.model} ({self.car.manufacturer.name})"
        )


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Country"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "NonExistent"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Manufacturer")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Manufacturer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "NonExistent"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Car")

    def test_driver_search(self):
        self.driver.first_name = "John"
        self.driver.last_name = "Doe"
        self.driver.save()

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "testdriver"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "John"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "Doe"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")


class FormTests(TestCase):
    def setUp(self):
        self.driver_data = {
            "username": "newdriver",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "New",
            "last_name": "Driver",
            "license_number": "ABC12345"
        }
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            license_number="XYZ98765"
        )

    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data=self.driver_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "newdriver")
        self.assertEqual(driver.license_number, "ABC12345")

    def test_driver_license_update_form_valid(self):
        driver = get_user_model().objects.create_user(
            username="license_update_driver",
            password="test12345",
            license_number="ABC12345"
        )
        form = DriverLicenseUpdateForm(
            data={"license_number": "NEW12345"},
            instance=driver
        )
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.license_number, "NEW12345")

    def test_car_form_valid(self):
        form = CarForm(data={
            "model": "New Car",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        })
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(car.model, "New Car")
        self.assertEqual(car.manufacturer, self.manufacturer)


class SearchEdgeCasesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_empty_search_query(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

    def test_case_insensitive_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Country"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "NonExistent"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Manufacturer")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Car"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Manufacturer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "NonExistent"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Car")

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "testdriver"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "John"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "Doe"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "Z_Z_Z_DEFINITELY_NOT_EXISTS_ANYWHERE"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no drivers in the service.")
