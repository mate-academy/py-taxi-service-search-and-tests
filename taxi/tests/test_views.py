from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


class PublicViewsTest(TestCase):
    """Test views that don't require authentication"""

    def test_login_required_driver_list(self):
        """Test that login is required for driver list"""
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")

    def test_login_required_car_list(self):
        """Test that login is required for car list"""
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_list(self):
        """Test that login is required for manufacturer list"""
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewsTest(TestCase):
    """Test views that require authentication for drivers"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        """Test retrieving driver list"""
        get_user_model().objects.create_user(
            username="driver1",
            password="pass123",
            license_number="DRV00001"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="pass123",
            license_number="DRV00002"
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail_view(self):
        """Test driver detail view"""
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PrivateCarViewsTest(TestCase):
    """Test views that require authentication for cars"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_retrieve_cars(self):
        """Test retrieving car list"""
        Car.objects.create(
            model="Model 3",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateManufacturerViewsTest(TestCase):
    """Test views that require authentication for manufacturers"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        """Test retrieving manufacturer list"""
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
