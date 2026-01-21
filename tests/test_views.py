from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer, Driver


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")


class CarListViewTest(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Toyota Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Toyota Corolla",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Honda Civic",
            manufacturer=self.manufacturer
        )

    def test_search_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Camry"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Camry")
        self.assertNotContains(response, "Toyota Corolla")
        self.assertNotContains(response, "Honda Civic")

    def test_empty_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Camry")
        self.assertContains(response, "Toyota Corolla")
        self.assertContains(response, "Honda Civic")

    def test_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars in taxi")


class ManufacturerListViewTest(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda")
        self.manufacturer3 = Manufacturer.objects.create(name="Ford")

    def test_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "Ford")

    def test_empty_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Honda")
        self.assertContains(response, "Ford")

    def test_no_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no manufacturers in the service."
        )


class DriverListViewTest(AuthTestCase):
    def setUp(self):
        super().setUp()
        user_model = get_user_model()
        self.driver1 = user_model.objects.create(
            username="john_doe",
            password="password",
            license_number="ABC12345"
        )
        self.driver2 = user_model.objects.create(
            username="jane_smith",
            password="password",
            license_number="XYZ67890"
        )
        self.driver3 = user_model.objects.create(
            username="sam_wilson",
            password="password",
            license_number="LMN54321"
        )

    def test_search_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")
        self.assertNotContains(response, "sam_wilson")

    def test_empty_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertContains(response, "jane_smith")
        self.assertContains(response, "sam_wilson")

    def test_no_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "Nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no drivers in the service.")
