from http.client import responses

from django.test import Client

from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        admin = get_user_model().objects.create_superuser(
            username="Test Admin",
            password="123456anton",
        )

        self.client.force_login(admin)

    @classmethod
    def setUpTestData(cls):
        number_manufacturer = 7

        for idx in range(number_manufacturer):
            Manufacturer.objects.create(
                name=f"Name {idx}",
                country=f"Country {idx}"
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_authors(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=2"
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_search(self):
        filter_part = "1"
        response = self.client.get(
            reverse("taxi:manufacturer-list") + f"?name={filter_part}"
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context["object_list"]) == 1)
        manufacturers = response.context["object_list"]

        for manufacturer in manufacturers:
            self.assertTrue(filter_part in manufacturer.name)

    def test_search_and_pagination(self):
        filter_part = "Name"
        response = self.client.get(
            reverse("taxi:manufacturer-list") + f"?name={filter_part}"
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context["object_list"]) == 5)
        manufacturers = response.context["object_list"]

        for manufacturer in manufacturers:
            self.assertTrue(filter_part in manufacturer.name)

        response = self.client.get(
            reverse("taxi:manufacturer-list") + f"?name={filter_part}&page=2"
        )
        self.assertTrue(response.status_code == 200)
        self.assertEqual(len(response.context["object_list"]), 2)


class DriverSearchForm(TestCase):
    def setUp(self):
        self.client = Client()
        admin = get_user_model().objects.create_superuser(
            username="Test Admin",
            password="123456anton",
        )
        self.client.force_login(admin)

    @classmethod
    def setUpTestData(cls):
        number_drivers = 7

        for idx in range(number_drivers):
            get_user_model().objects.create_user(
                username=f"Test username {idx}",
                license_number=f"Test license number {idx}"
            )

    def test_search_and_pagination(self):
        url = reverse("taxi:driver-list")
        filter_part = "1"
        response = self.client.get(url + f"?username={filter_part}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)


class CarSearchForm(TestCase):
    def setUp(self):
        self.client = Client()
        admin = get_user_model().objects.create_superuser(
            username="Test",
            password="Test"
        )
        self.client.force_login(admin)

    @classmethod
    def setUpTestData(cls):
        number_cars = 8
        manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )

        for idx in range(number_cars):
            Car.objects.create(
                model=f"Test_model {idx}",
                manufacturer=manufacturer
            )

    def test_search_and_pagination(self):
        url = reverse("taxi:car-list")
        filter_part = "1"
        cars = Car.objects.filter(model__icontains=f"{filter_part}")
        response_1 = self.client.get(url + "?page=1")
        response_2 = self.client.get(url + "?page=2")
        response_search = self.client.get(url + f"?model={filter_part}")

        self.assertEqual(len(response_1.context["object_list"]), 5)
        self.assertEqual(len(response_2.context["object_list"]), 3)
        self.assertEqual(len(response_search.context["object_list"]), 1)
        self.assertEqual(
            list(response_search.context["object_list"]),
            list(cars)
        )
