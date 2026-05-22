from django import test
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class TestPublicManufacturerView(test.TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class TestPrivateManufacturerView(test.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")
        self.url = reverse("taxi:manufacturer-list")

    def test_retrieve_manufacturers(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(self.url, data={"search": "yota"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")


class TestPublicCarView(test.TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class TestPrivateCarView(test.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        Car.objects.create(model="Focus", manufacturer=self.manufacturer)
        Car.objects.create(model="Mustang", manufacturer=self.manufacturer)
        self.url = reverse("taxi:car-list")

    def test_retrieve_cars(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Focus")
        self.assertContains(response, "Mustang")

    def test_search_car_by_model(self):
        response = self.client.get(self.url, data={"search": "mus"})
        self.assertContains(response, "Mustang")
        self.assertNotContains(response, "Focus")


class TestPublicDriverView(test.TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class TestPrivateDriverView(test.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="jack.daniels",
            password="password123",
            license_number="DDD44444"
        )
        get_user_model().objects.create_user(
            username="john.doe",
            password="password123",
            license_number="EEE55555"
        )
        self.url = reverse("taxi:driver-list")

    def test_retrieve_drivers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jack.daniels")
        self.assertContains(response, "john.doe")

    def test_search_driver_by_username(self):
        response = self.client.get(self.url, data={"search": "jack"})
        self.assertContains(response, "jack.daniels")
        self.assertNotContains(response, "john.doe")
