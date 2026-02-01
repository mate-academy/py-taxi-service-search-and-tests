from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car


class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="test3",
            country="testCountry",
        )
        Manufacturer.objects.create(
            name="test4",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="test5",
            country="Germany",
        )
        driver1 = get_user_model().objects.create(
            username="Tom",
            password="<PASSWORD>",
            license_number="AAA12121",
            first_name="Driver",
            last_name="TestDriver",
        )
        driver2 = get_user_model().objects.create(
            username="John",
            password="<PASSWORD>",
            license_number="BBB15454",
            first_name="Driver",
            last_name="TestDriver",
        )
        driver3 = get_user_model().objects.create(
            username="Maks",
            password="<PASSWORD>",
            license_number="CVD43434",
            first_name="Driver",
            last_name="TestDriver",
        )

        car1 = Car.objects.create(
            model="BMW X5M",
            manufacturer=manufacturer1,
        )
        car1.drivers.add(driver1, driver2)
        car2 = Car.objects.create(
            model="Audi A8",
            manufacturer=manufacturer2,
        )
        car2.drivers.add(driver2, driver3)

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="king_Julian",
            password="adminadmin",
        )
        self.client.force_login(self.admin_user)

    def test_manufacturer_list_view_without_search_params(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["manufacturer_list"])
        self.assertTrue(response.context["search_form"])
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_manufacturer_list_view_with_search_params(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name":"M"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["manufacturer_list"][0]), "BMW Germany")
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm,
        )
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertEqual(response.context["search_form"].initial["name"], "M")

    def test_driver_list_view_without_search_params(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["driver_list"])
        self.assertTrue(response.context["search_form"])
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_driver_list_view_with_search_params(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "M"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm,
        )
        self.assertEqual(len(response.context["driver_list"]), 2)
        self.assertEqual(response.context["search_form"].initial["username"], "M")

    def test_car_list_view_without_search_params(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["car_list"])
        self.assertTrue(response.context["search_form"])
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_car_list_view_with_search_params(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "BMW"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            CarSearchForm,
        )
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["search_form"].initial["model"], "BMW")
