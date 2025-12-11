from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer, Driver


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        Car.objects.create(model="Toyota", manufacturer=manufacturer)
        Car.objects.create(model="Kia", manufacturer=manufacturer)
        Car.objects.create(model="Mercedes", manufacturer=manufacturer)

    def test_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Toy")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Kia")
        self.assertNotContains(response, "Mercedes")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="Test1234"
        )
        self.client.login(username="testuser", password="Test1234")
        Driver.objects.create_user(
            username="John_Doe",
            password="test1234",
            license_number="XYZ12345",
            first_name="John",
            last_name="Doe"
        )

        Driver.objects.create_user(
            username="Alex_Black",
            password="test1234",
            license_number="XYZ12545",
            first_name="Alex",
            last_name="Black"
        )

    def test_search_by_username(self):
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?username=Joh")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")
        self.assertNotContains(response, "Alex_Black")
