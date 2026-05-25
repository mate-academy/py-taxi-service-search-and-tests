from django.test import TestCase

from django.contrib.auth import (
    get_user_model,
)
from django.urls import reverse

from taxi.models import (
    Car,
    Manufacturer,
)


class PublicViewsTest(
    TestCase
):
    def test_login_required(
        self,
    ):
        response = self.client.get(
            reverse(
                "taxi:driver-list"
            )
        )

        self.assertNotEqual(
            response.status_code,
            200,
        )


class DriverSearchTests(
    TestCase
):
    def setUp(self) -> None:
        self.user = (
            get_user_model()
            .objects.create_user(
                username="admin",
                password="12345",
                license_number="AAA11111",
            )
        )

        (
            get_user_model()
            .objects.create_user(
                username="john",
                password="12345",
                license_number="BBB22222",
            )
        )

        (
            get_user_model()
            .objects.create_user(
                username="maria",
                password="12345",
                license_number="CCC33333",
            )
        )

        self.client.force_login(
            self.user
        )

    def test_search_driver(
        self,
    ) -> None:
        response = self.client.get(
            reverse(
                "taxi:driver-list"
            ),
            {"username": "john"},
        )

        queryset = response.context[
            "driver_list"
        ]

        self.assertEqual(
            len(queryset),
            1,
        )

        self.assertEqual(
            queryset[0].username,
            "john",
        )


class CarSearchTests(
    TestCase
):
    def setUp(self):
        self.user = (
            get_user_model()
            .objects.create_user(
                username="admin",
                password="12345",
            )
        )

        manufacturer = (
            Manufacturer.objects.create(
                name="BMW",
                country="Germany",
            )
        )

        Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )

        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )

        self.client.force_login(
            self.user
        )

    def test_search_car(
        self,
    ):
        response = self.client.get(
            reverse(
                "taxi:car-list"
            ),
            {"model": "X5"},
        )

        queryset = response.context[
            "car_list"
        ]

        self.assertEqual(
            len(queryset),
            1,
        )

        self.assertEqual(
            queryset[0].model,
            "X5",
        )


class ManufacturerSearchTests(
    TestCase
):
    def setUp(self):
        self.user = (
            get_user_model()
            .objects.create_user(
                username="admin",
                password="12345",
            )
        )

        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.client.force_login(
            self.user
        )

    def test_search_manufacturer(
        self,
    ):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-list"
            ),
            {"name": "BMW"},
        )

        queryset = response.context[
            "manufacturer_list"
        ]

        self.assertEqual(
            len(queryset),
            1,
        )
