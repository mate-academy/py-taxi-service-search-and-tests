from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer

User = get_user_model()


class PublicViewsTests(TestCase):
    def test_login_required_for_lists(self):
        urls = (
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)
                self.assertIn("/accounts/login/", response.url)


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password="test-password",
            license_number="AAA12345",
        )
        User.objects.create_user(
            username="john_driver",
            password="test-password",
            license_number="BBB12345",
        )
        User.objects.create_user(
            username="mike_driver",
            password="test-password",
            license_number="CCC12345",
        )

        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")

        Car.objects.create(model="Camry", manufacturer=toyota)
        Car.objects.create(model="X5", manufacturer=bmw)

    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "mike_driver")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "cam"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_empty_search_returns_all_objects(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "BMW")

    def test_search_query_is_kept_during_pagination(self):
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Ukraine",
        )
        for number in range(6):
            Car.objects.create(
                model=f"Searchable car {number}",
                manufacturer=manufacturer,
            )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "Searchable"},
        )

        self.assertContains(response, "query=Searchable&amp;page=2")


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)

        self.assertEqual(str(car), "Camry")

    def test_driver_str(self):
        driver = User.objects.create_user(
            username="john_driver",
            password="test-password",
            first_name="John",
            last_name="Doe",
            license_number="AAA12345",
        )

        self.assertEqual(str(driver), "john_driver (John Doe)")


class DriverFormsTests(TestCase):
    def test_driver_creation_form_with_valid_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "new_driver",
                "password1": "StrongTestPass123",
                "password2": "StrongTestPass123",
                "first_name": "New",
                "last_name": "Driver",
                "license_number": "ABC12345",
            }
        )

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_with_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)