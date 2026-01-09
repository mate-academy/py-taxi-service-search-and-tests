from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class PublicViewsTests(TestCase):
    """Test views that don't require authentication"""

    def setUp(self):
        self.client = Client()

    def test_login_required_driver_list(self):
        """Test that login is required for driver list"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_login_required_car_list(self):
        """Test that login is required for car list"""
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 302)

    def test_login_required_manufacturer_list(self):
        """Test that login is required for manufacturer list"""
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 302)


class PrivateDriverViewsTests(TestCase):
    """Test views that require authentication for drivers"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

        # Create test drivers
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="pass123",
            license_number="DRV001",
            first_name="John",
            last_name="Doe"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="pass123",
            license_number="DRV002",
            first_name="Jane",
            last_name="Smith"
        )

    def test_driver_list_view(self):
        """Test driver list view works"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_contains_drivers(self):
        """Test driver list contains created drivers"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    def test_driver_detail_view(self):
        """Test driver detail view works"""
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.driver1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)


class PrivateCarViewsTests(TestCase):
    """Test views that require authentication for cars"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_car_list_view(self):
        """Test car list view works"""
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_contains_cars(self):
        """Test car list contains created cars"""
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")

    def test_car_detail_view(self):
        """Test car detail view works"""
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")


class PrivateManufacturerViewsTests(TestCase):
    """Test views that require authentication for manufacturers"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_manufacturer_list_view(self):
        """Test manufacturer list view works"""
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_contains_manufacturers(self):
        """Test manufacturer list contains created manufacturers"""
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Honda")
        self.assertContains(response, "Ford")


class IndexViewTest(TestCase):
    """Test index view"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        """Test index view works"""
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_counts(self):
        """Test index displays correct counts"""
        Manufacturer.objects.create(name="Test", country="Test")
        response = self.client.get(reverse("taxi:index"))

        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
