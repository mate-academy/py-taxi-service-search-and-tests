from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class TetCarSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        models = ["ford ka", "audi a6", "audi tt", "bmw x5"]
        for model in models:
            for number in range(len(models)):
                Car.objects.create(
                    model=f"{model}_{number}",
                    manufacturer=manufacturer
                )

    def test_search_with_first_paginate_page(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search_data=audi"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list((response.context["car_list"])),
            list(Car.objects.filter(model__icontains="audi"))[:5]
        )

    def test_search_with_last_paginate_page(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search_data=audi&page=2"
        )
        self.assertEqual(
            list((response.context["car_list"])),
            list(Car.objects.filter(model__icontains="audi"))[-3:])

    def test_search_without_pagination(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search_data=bmw"
        )
        self.assertEqual(
            list((response.context["car_list"])),
            list(Car.objects.filter(model__icontains="bmw")))

    def test_search_with_no_result(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search_data=zaz"
        )
        self.assertEqual(
            list((response.context["car_list"])), [])


class TestManufacturerSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)

        manufacturers = [
            "fiat",
            "ford",
            "ferrari",
            "DAF",
            "Alfa Romeo",
            "Infiniti",
            "Acura",
            "Man",
            "Wiesmann"
        ]

        for manufacturer in manufacturers:
            Manufacturer.objects.create(
                name=manufacturer,
                country="Land of Oz"
            )

    def test_search_manufacturer_with_first_paginate_page(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search_data=f"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list((response.context["manufacturer_list"])),
            list(Manufacturer.objects.filter(name__icontains="f"))[:5]
        )

    def test_search_manufacturer_with_last_paginate_page(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search_data=f&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list((response.context["manufacturer_list"])),
            list(Manufacturer.objects.filter(name__icontains="f"))[-1:]
        )

    def test_search_manufacturer_without_pagination(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search_data=man"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list((response.context["manufacturer_list"])),
            list(Manufacturer.objects.filter(name__icontains="man")))

    def test_search_with_no_result(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search_data=abra"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list((response.context["manufacturer_list"])), []
        )
