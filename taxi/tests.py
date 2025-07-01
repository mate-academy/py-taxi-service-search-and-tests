from django.test import TestCase
from django.urls import reverse

from .models import Car, Driver, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        # Создаём пользователя правильно
        self.user = Driver.objects.create_user(username="testuser", password="12345")

        logged_in = self.client.login(username="testuser", password="12345")
        print("Logged in:", logged_in)
        assert logged_in, "Не удалось залогиниться в тестах!"

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        Car.objects.create(model="Camry", manufacturer=Manufacturer.objects.first())
        Car.objects.create(model="X5", manufacturer=Manufacturer.objects.last())

        Driver.objects.create_user(
            username="ivanov", password="pass123", license_number="123456"
        )
        Driver.objects.create_user(
            username="petrov", password="pass123", license_number="654321"
        )

    def test_search_manufacturer(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"q": "Toy"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_car(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "Cam"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_search_driver(self):
        response = self.client.get(reverse("taxi:driver-list"), {"q": "ivan"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ivanov")
        self.assertNotContains(response, "petrov")
