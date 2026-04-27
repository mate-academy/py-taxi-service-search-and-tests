from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="US",
        )
        Car.objects.create(
            model="Toyota",
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "driver241",
            "password2": "driver241",
            "license_number": "BGD51353",
        }
        self.client.post(reverse("taxi:driver-create"),
                         data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"])
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"])


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        self.manufacturer1 = Manufacturer.objects.create(
            name="Ford", country="Falcon")
        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer)

    def test_retrieve_index_page(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_cars"], 2)
        self.assertEqual(response.context["num_visits"], 1)

    def test_car_search_filter(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "Camry"}
        )
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_manufacturer_search_filter(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"name": "Toyota"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertIn("search_form", response.context)

    def test_assign_driver_to_car(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car1.pk})

        self.client.get(url)
        self.assertIn(self.car1, self.user.cars.all())

        self.client.get(url)
        self.assertNotIn(self.car1, self.user.cars.all())


class PaginationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="123")
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Test")
        for i in range(15):
            Car.objects.create(model=f"Model-{i}", manufacturer=manufacturer)

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)
