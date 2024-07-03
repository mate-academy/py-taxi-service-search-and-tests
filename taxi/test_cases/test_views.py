from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicViewsTest(TestCase):
    def setUp(self):
        self.manufacturer_list_url = reverse("taxi:manufacturer-list")
        self.manufacturer_create_url = reverse("taxi:manufacturer-create")
        self.car_list_url = reverse("taxi:car-list")
        self.car_create_url = reverse("taxi:car-create")
        self.driver_list_url = reverse("taxi:driver-list")
        self.driver_create_url = reverse("taxi:driver-create")

    def test_login_required(self):
        urls = [
            self.manufacturer_list_url,
            self.manufacturer_create_url,
            self.car_list_url,
            self.car_create_url,
            self.driver_list_url,
            self.driver_create_url,
        ]

        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test134"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.manufacturer = Manufacturer.objects.create(name="Ford")
        self.car = Car.objects.create(
            model="testmodel",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_car_list_view_search(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "testmodel"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.manufacturer.name)
        self.assertContains(response, self.car.model)

    def test_car_list_view_pagination(self):
        manufacturer = Manufacturer.objects.create(name="Toyota")
        cars = [
            Car.objects.create(
                model=f"model{i}",
                manufacturer=manufacturer
            )
            for i in range(3)
        ]
        for car in cars:
            car.drivers.add(self.user)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertTrue(response.context["is_paginated"])


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test2", password="testpass2"
        )
        self.client.force_login(self.user)

    def test_creation_drivers(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "test Last",
            "license_number": "TES12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
