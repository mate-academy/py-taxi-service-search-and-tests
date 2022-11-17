from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class PublicDriverTest(TestCase):
    def test_login_required(self):
        resp = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(resp.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        resp = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(resp.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(resp.status_code, 200)


class ViewsTests(TestCase):
    def setUp(self) -> None:
        number_of_cars = 10

        for car_id in range(number_of_cars):
            manufacturer = Manufacturer.objects.create(
                name=f"Name {car_id}",
                country=f"Country {car_id}"
            )

            Car.objects.create(
                model=f"Car_model {car_id}",
                manufacturer=manufacturer
            )

            Driver.objects.create(
                username=f"username {car_id}",
                license_number=f"ABC1234{car_id}"
            )

        self.driver = get_user_model().objects.create_user(
            "test_user",
            "password123"
        )
        self.client.force_login(self.driver)

    def test_car_get_context_data(self) -> None:
        response = self.client.get(reverse("taxi:car-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertTrue("car_search" in response.context)
        self.assertTrue("model" in response.context["car_search"].fields)

    def test_manufacturer_get_context_data(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertTrue("manufacturer_search" in response.context)
        self.assertTrue(
            "name" in response.context["manufacturer_search"].fields
        )

    def test_driver_get_context_data(self) -> None:
        response = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)
        self.assertTrue("driver_search" in response.context)
        self.assertTrue(
            "username" in response.context["driver_search"].fields
        )

    def test_driver_get_queryset(self) -> None:
        response = self.client.get("/drivers/?username=test")
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="test")
        )

    def test_car_get_queryset(self) -> None:
        response = self.client.get("/cars/?model=test")
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="test")
        )

    def test_manufacturer_get_queryset(self) -> None:
        response = self.client.get("/manufacturers/?name=test")
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="test")
        )
