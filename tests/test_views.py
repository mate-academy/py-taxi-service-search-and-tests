from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from taxi.forms import ManufacturerSearchForm
from taxi.models import Driver, Manufacturer, Car


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("taxi:index")

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="driver1",
            password="12345",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_index_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Best Taxi Ever!")
        self.assertContains(response, "Drivers")
        self.assertContains(response, "Cars")
        self.assertContains(response, "Manufacturers")
        self.assertContains(response, "You have visited this page")

    def test_index_view_without_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class ToggleAssignCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="jon.doe",
            first_name="John",
            last_name="Doe",
            email="john@taxi.com",
            license_number="ABC12345"
        )
        self.driver.cars.add(self.car)

    def test_toggle_assign_to_car_view(self):
        self.client.login(username="testuser", password="password")
        url = reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])

        # Test assigning car to driver
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Test unassigning car from driver
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.driver.cars.filter(pk=self.car.pk).exists())
