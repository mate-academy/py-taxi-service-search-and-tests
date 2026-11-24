from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer, Driver

User = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="testauthor",
            license_number="HGU12345"
            # pseudonym="Test Pseudonym",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "HGU12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_driver",
            password="testpassword123",
        )
        self.client.force_login(self.user)

    def test_search_by_model_returns_matching_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        matching_car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Civic",
            manufacturer=manufacturer,
        )
        response = self.client.get(
            reverse("taxi:car-list"),  # заміни на назву свого URL
            {"model": "cor"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Civic")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.matching_driver = Driver.objects.create_user(
            username="john_smith",
            password="test-password",
            license_number="HGU12345",
        )
        self.other_driver = Driver.objects.create_user(
            username="alice",
            password="test-password",
            license_number="UIG12345",
        )
        self.client.force_login(self.matching_driver)

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),  # заміни на ім'я URL зі свого urls.py
            {"username": "JOHN"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_smith")
        self.assertNotContains(response, "alice")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        self.user = User.objects.create_user(
            username="test_driver",
            password="testpassword123",
        )
        self.client.force_login(self.user)

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),  # заміни на ім'я URL зі свого urls.py
            {"name": "toy"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
