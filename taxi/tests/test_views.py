from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver

User = get_user_model()


class PublicViewsTest(TestCase):
    def test_login_required_redirect(self):
        """
        Test that all views require
        login and redirect unauthorized users.
        """
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next=/'
        )


class PrivateViewsTest(TestCase):
    def setUp(self):
        """Create a user and log them in."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_index_view(self):
        """Test index view and context data."""
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertIn("num_visits", response.context)

    def test_manufacturer_list_view(self):
        """Test manufacturer list view with search."""
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Toyota"}
        )
        self.assertContains(response, "Toyota")

        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"search": "Ford"}
        )
        self.assertNotContains(response, "Toyota")

    def test_car_list_view(self):
        """Test car list view with search functionality."""
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Camry"}
        )
        self.assertContains(response, "Camry")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Corolla"}
        )
        self.assertNotContains(response, "Camry")

    def test_driver_list_view(self):
        """Test driver list view with search functionality."""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "driver1"}
        )
        self.assertContains(response, "driver1")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "driver2"}
        )
        self.assertNotContains(response, "driver1")

    def test_toggle_assign_to_car(self):
        """Test toggling assignment of a driver to a car."""
        self.client.force_login(self.driver)

        self.assertNotIn(self.car, self.driver.cars.all())

        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertIn(self.car, self.driver.cars.all())

        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertNotIn(self.car, self.driver.cars.all())

    def test_create_manufacturer_view(self):
        """Test the manufacturer creation view."""
        form_data = {"name": "Honda", "country": "Japan"}
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_update_manufacturer_view(self):
        """Test the manufacturer update view."""
        form_data = {"name": "Toyota", "country": "USA"}
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.country, "USA")

    def test_delete_manufacturer_view(self):
        """Test the manufacturer delete view."""
        response = self.client.post(
            reverse("taxi:manufacturer-delete",
                    args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(
            id=self.manufacturer.id
        ).exists())
