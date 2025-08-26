from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Driver, Car, Manufacturer
from .forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    validate_license_number
)


class ModelTest(TestCase):
    """Test cases for models."""

    def setUp(self):
        """Set up test data."""
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        """Test manufacturer string representation."""
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_driver_str(self):
        """Test driver string representation."""
        self.assertEqual(str(self.driver), "testdriver (John Doe)")

    def test_car_str(self):
        """Test car string representation."""
        self.assertEqual(str(self.car), "Camry")

    def test_car_driver_relationship(self):
        """Test many-to-many relationship between car and drivers."""
        self.car.drivers.add(self.driver)
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())


class LicenseValidationTest(TestCase):
    """Test cases for license number validation."""

    def test_valid_license_number(self):
        """Test valid license number passes validation."""
        valid_license = "ABC12345"
        result = validate_license_number(valid_license)
        self.assertEqual(result, valid_license)

    def test_invalid_length(self):
        """Test license number with invalid length."""
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_invalid_format_letters(self):
        """Test license number with invalid letter format."""
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")


class FormTest(TestCase):
    """Test cases for forms."""

    def test_driver_creation_form_valid(self):
        """Test valid driver creation form."""
        form_data = {
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_forms(self):
        """Test search forms."""
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")

        form = CarSearchForm(data={"model": "camry"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "camry")

        form = ManufacturerSearchForm(data={"name": "toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "toyota")


class ViewTest(TestCase):
    """Test cases for views."""

    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_index_view_authenticated(self):
        """Test index view for authenticated user."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Drivers:")
        self.assertIn("num_drivers", response.context)

    def test_index_view_unauthenticated(self):
        """Test index view redirects unauthenticated users."""
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)

    def test_list_views(self):
        """Test list views."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_detail_views(self):
        """Test detail views."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)


class SearchTest(TestCase):
    """Test cases for search functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_driver_search(self):
        """Test driver search functionality."""
        self.client.login(username="testuser", password="testpass123")

        Driver.objects.create_user(
            username="anotherdriver",
            password="testpass123",
            license_number="XYZ98765"
        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertNotContains(response, "anotherdriver")

    def test_car_search(self):
        """Test car search functionality."""
        self.client.login(username="testuser", password="testpass123")

        Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_manufacturer_search(self):
        """Test manufacturer search functionality."""
        self.client.login(username="testuser", password="testpass123")

        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")


class SecurityTest(TestCase):
    """Test cases for security and permissions."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access protected views."""
        protected_views = [
            "taxi:driver-list",
            "taxi:car-list",
            "taxi:manufacturer-list",
        ]

        for view_name in protected_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)


class CRUDTest(TestCase):
    """Test cases for CRUD operations."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_create(self):
        """Test manufacturer creation."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("taxi:manufacturer-create"), {
            "name": "BMW",
            "country": "Germany"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="BMW").exists())

    def test_toggle_assign_to_car(self):
        """Test toggle assign to car functionality."""
        self.client.login(username="testuser", password="testpass123")

        car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

        self.assertNotIn(self.user, car.drivers.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, car.drivers.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, car.drivers.all())
