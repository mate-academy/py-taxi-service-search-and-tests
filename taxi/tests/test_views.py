from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_manufacturer_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_cars_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )
        self.client.force_login(self.user)

    def test_drivers_listed(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_cars_listed(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        Car.objects.create(
            model="Cybertruck",
            manufacturer=manufacturer
        )
        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_manufacturers_listed(self):
        Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_5(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        for _ in range(13):
            Car.objects.create(
                model="test",
                manufacturer=manufacturer
            )
        response = self.client.get(reverse("taxi:car-list") + "?page=3")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 3)


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=Manufacturer.objects.create(
                name="Tesla",
                country="USA"
            )
        )
        self.client.force_login(self.user)

    def test_toggle_assign_to_car_add(self):

        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.cars.filter(pk=self.car.pk).exists())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car)
        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.cars.filter(pk=self.car.pk).exists())
