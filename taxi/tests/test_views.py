from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Manufacturer, Car


class DriverListViewTest(TestCase):
    def setUp(self):

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            license_number="ABC12345",
            password="password123"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            license_number="DEF67890",
            password="password123"
        )
        self.client.login(username="driver1", password="password123")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(
            response.status_code, 302
        )
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('taxi:driver-list')}"
        )

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_search_with_empty_username(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    def test_search_form_in_context(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )

    def test_pagination_is_five(self):
        for i in range(6):
            get_user_model().objects.create_user(
                username=f"driver{i+3}",
                license_number=f"XYZ{i+3}1234",
                password="password123",
            )

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_pagination_second_page(self):
        for i in range(6):
            get_user_model().objects.create_user(
                username=f"driver{i+3}",
                license_number=f"XYZ{i+3}1234",
                password="password123",
            )

        response = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["driver_list"]), 3
        )


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="password123"
        )
        self.client.login(username="tester", password="password123")

        for i in range(8):
            Manufacturer.objects.create(name=f"Manufacturer{i+1}")

    def test_pagination_first_page(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 5
        )

    def test_pagination_second_page(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 3
        )

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Manufacturer1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "NonExistentManufacturer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")

    def test_search_empty_query(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 5
        )


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="password123"
        )
        self.client.login(username="tester", password="password123")

        self.manufacturer1 = Manufacturer.objects.create(name="Manufacturer1")
        self.manufacturer2 = Manufacturer.objects.create(name="Manufacturer2")

        for i in range(8):
            Car.objects.create(
                model=f"Model{i+1}",
                manufacturer=self.manufacturer1 if i % 2 == 0
                else self.manufacturer2,
            )

    def test_pagination_first_page(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["car_list"]), 5
        )

    def test_pagination_second_page(self):
        response = self.client.get(reverse("taxi:car-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["car_list"]), 3
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Model1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model1")
        self.assertNotContains(response, "Model2")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "NonExistentModel"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Model1")
        self.assertNotContains(response, "Model2")

    def test_search_empty_query(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["car_list"]), 5
        )
