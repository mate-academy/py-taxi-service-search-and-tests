from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="user", password="pass123"
        )
        self.manufacturer = (
            Manufacturer.objects.create(name="Toyota", country="Japan")
        )

    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_create_car_with_invalid_data(self):
        self.client.login(username="user", password="pass123")
        url = reverse("taxi:car-create")
        data = {
            "model": "",
            "manufacturer": self.manufacturer.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertEqual(Car.objects.count(), 0)


class ManufacturerListViewTestCase(TestCase):
    def setUp(self):
        self.user = (
            Driver.objects.create_user(username="user", password="pass123")
        )
        self.url = reverse("taxi:manufacturer-list")
        self.manufacturer1 = Manufacturer.objects.create(name="Manufacturer 1")
        self.manufacturer2 = Manufacturer.objects.create(name="Manufacturer 2")

    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_view_for_logged_in_user(self):
        self.client.login(username="user", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.manufacturer1, response.context["manufacturer_list"]
        )
        self.assertIn(
            self.manufacturer2, response.context["manufacturer_list"]
        )


#
class DriverListViewTestCase(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser", password="password123"
        )
        self.url = reverse("taxi:driver-list")
        self.driver = Driver.objects.create(
            username=self.user, license_number="ABC12345"
        )
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_view_for_logged_in_user(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("driver_list", response.context)
        self.assertIn(self.driver, response.context["driver_list"])
        self.assertContains(response, self.driver.license_number)
