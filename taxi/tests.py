from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Manufacturer, Car


class PublicAccessTest(TestCase):
    def test_login_required_for_list_views(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass", license_number="TEST123"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        Driver.objects.create_user(
            username="john", password="1234", license_number="AAA111"
        )
        Driver.objects.create_user(
            username="jack", password="1234", license_number="BBB222"
        )

        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "john"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertNotContains(response, "jack")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="M3", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-list"), {"model": "X5"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertNotContains(response, "M3")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "Toyota"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
