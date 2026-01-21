from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123"
        )
        self.client.force_login(self.user)
        for i in range(10):
            Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country=f"Country {i}"
            )

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        if response.context["is_paginated"]:
            per_page = response.context["paginator"].per_page
            self.assertQuerysetEqual(
                response.context["manufacturer_list"],
                manufacturers[:per_page]
            )
        else:
            self.assertQuerysetEqual(
                response.context["manufacturer_list"],
                manufacturers
            )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_pagination(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(
            len(response.context["manufacturer_list"]), 5
        )

    def test_context_data(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?manufacturer=Manufacturer 1"
        )
        self.assertEqual(
            response.context["form"].initial["manufacturer"],
            "Manufacturer 1"
        )

    def test_queryset(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?manufacturer=Manufacturer 1"
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]), 1
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Manufacturer 1"
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )

        for i in range(10):
            Car.objects.create(
                model=f"Car {i}",
                manufacturer=manufacturer,
            )

    def test_retrieve_car(self) -> None:
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        if response.context["is_paginated"]:
            per_page = response.context["paginator"].per_page
            self.assertEqual(
                list(response.context["car_list"]),
                list(cars[:per_page])
            )
        else:
            self.assertEqual(
                list(response.context["car_list"]),
                list(cars)
            )
        self.assertTemplateUsed(
            response, "taxi/car_list.html"

        )

    def test_pagination(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(
            len(response.context["car_list"]), 5
        )

    def test_context_data(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model_name=Car 1"
        )
        self.assertEqual(
            response.context["form"].initial["model_name"],
            "Car 1"
        )

    def test_queryset(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model_name=Car 1"
        )
        self.assertEqual(
            len(response.context["car_list"]), 1
        )
        self.assertEqual(
            response.context["car_list"][0].model,
            "Car 1"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123"
        )
        self.client.force_login(self.user)

        for i in range(10):
            Driver.objects.create(
                username=f"driver{i}",
                password=f"testdriverpass{i}",
                license_number=f"ABC{i}2345"
            )

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        if response.context["is_paginated"]:
            per_page = response.context["paginator"].per_page
            self.assertEqual(
                list(response.context["driver_list"]),
                list(drivers[:per_page])
            )
        else:
            self.assertEqual(
                list(response.context["driver_list"]),
                list(drivers)
            )
        self.assertTemplateUsed("taxi/driver_list.html")

    def test_pagination(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(
            len(response.context["driver_list"]), 5
        )

    def test_context_data(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?driver=driver1"
        )
        self.assertEqual(
            response.context["form"].initial["driver"],
            "driver1"
        )

    def test_queryset(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?driver=driver1"
        )
        self.assertEqual(
            len(response.context["driver_list"]), 1
        )
        self.assertEqual(
            response.context["driver_list"][0].username,
            "driver1"
        )
        self.assertEqual(
            response.context["driver_list"][0].license_number,
            "ABC12345"

        )
