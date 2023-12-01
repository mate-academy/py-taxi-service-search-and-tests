from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="driveruser",
            license_number="ABC12345"
        )

    def test_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

    def test_manufacturer_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)

    # Add similar tests for ManufacturerCreateView,
    # ManufacturerUpdateView, ManufacturerDeleteView, etc.

    def test_car_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

    # Add similar tests for CarDetailView,
    # CarCreateView, CarUpdateView, CarDeleteView, etc.

    def test_driver_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

    # Add similar tests for DriverDetailView, DriverCreateView,
    # DriverLicenseUpdateView, DriverDeleteView, etc.

    def test_toggle_assign_to_car_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_index_view_unauthenticated(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("taxi:index")
        )

    def test_manufacturer_list_view_unauthenticated(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("taxi:manufacturer-list")
        )

        # Add similar tests for other views (car, driver, etc.)
