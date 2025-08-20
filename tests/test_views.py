from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import (
    Manufacturer,
    Car,
    Driver
)

User = get_user_model()


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:manufacturer-list')}"
        )

    def test_list_view_without_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_list_view_with_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"}
        )
        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturer_list), 1)
        self.assertEqual(manufacturer_list[0].name, "Toyota")

    def test_pagination(self):
        for i in range(10):
            Manufacturer.objects.create(
                name=f"Name_{i}", country=f"Country_{i}"
            )

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:car-list')}"
        )

    def test_list_view_without_search(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 2)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Camry")

    def test_list_view_with_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Cam"})
        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 1)
        self.assertEqual(car_list[0].model, "Camry")

    def test_pagination(self):
        for i in range(10):
            Car.objects.create(
                model=f"Name_{i}",
                manufacturer=self.manufacturer
            )

        response = self.client.get(reverse("taxi:car-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        Driver.objects.create(username="alice", license_number="AAA12345")
        Driver.objects.create(username="bob", license_number="BBB12345")

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:driver-list')}"
        )

    def test_list_view_without_search(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 3)
        self.assertContains(response, "alice")
        self.assertContains(response, "bob")

    def test_list_view_with_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ali"}
        )
        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 1)
        self.assertEqual(driver_list[0].username, "alice")

    def test_pagination(self):
        for i in range(10):
            Driver.objects.create(
                username=f"Username_{i}",
                license_number=f"QWE0000{i}"
            )

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)
