from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ManufacturerTestViews(TestCase):

    def setUp(self):

        for number in range(10):
            Manufacturer.objects.create(
                name=f"Manufacturer {number}",
                country=f"Country {number}"
            )
        self.user = get_user_model().objects.create(
            username="Test",
            password="1qazxsw",
        )
        self.client.force_login(self.user)

    def test_view_pagination_is_5(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 5
        )

    def test_view_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )

    def test_view_correct_context_data_with_data(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "Test Manufacturer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "Test Manufacturer"
        )

    def test_view_correct_context_data_without_data(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["name"], "")


class CarTestViews(TestCase):

    def setUp(self):
        for number in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"Manufacturer {number}",
                country=f"Country {number}"
            )

            Car.objects.create(
                model=f"Test Car {number}",
                manufacturer=manufacturer,
            )

        self.user = get_user_model().objects.create(
            username="Test",
            password="1qazxsw",
        )
        self.client.force_login(self.user)

    def test_view_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_view_pagination_is_5(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_view_correct_context_data_with_data(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Test Car"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["model"], "Test Car"
        )

    def test_view_correct_context_data_without_data(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["model"], "")


class DriverTestViews(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(
            username="Test",
            first_name="First name",
            last_name="Last name",
            email="Email",
        )
        self.client.force_login(user)

    def test_view_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_view_correct_context_data_with_data(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Test Username"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "Test Username"
        )

    def test_view_correct_context_data_without_data(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], ""
        )
