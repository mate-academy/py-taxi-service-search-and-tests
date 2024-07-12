from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Driver, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicAccessViewTest(TestCase):
    def test_index_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2F")

    def test_manufacturer_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fmanufacturers%2F"
        )

    def test_car_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fcars%2F"
        )

    def test_driver_list_login_required_and_redirect_to_login_page(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fdrivers%2F"
        )


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_counts(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Toyota Camry", manufacturer_id=1)

        response = self.client.get(INDEX_URL)

        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)

    def test_visits_tracking(self):
        for _ in range(3):
            self.client.get(INDEX_URL)

        response = self.client.get(INDEX_URL)

        self.assertEqual(response.context["num_visits"], 4)
        self.assertEqual(self.client.session.get("num_visits"), 4)

    def test_template_used(self):
        response = self.client.get(INDEX_URL)
        self.assertTemplateUsed(response, "taxi/index.html")


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

        for index in range(1, 8):
            Manufacturer.objects.create(
                name=f"Test Manufacturer{index}",
                country=f"Test Country{index}",
            )
        self.all_manufacturers = Manufacturer.objects.all()
        self.response_manufacturer_p1 = self.client.get(MANUFACTURER_LIST_URL)
        self.response_manufacturer_p2 = self.client.get(
            MANUFACTURER_LIST_URL,
            {"page": 2}
        )
        self.manufacturer_2_pages = (
            list(
                self.response_manufacturer_p1.context["manufacturer_list"]
            )
            + list(
                self.response_manufacturer_p2.context["manufacturer_list"]
            )
        )

        self.response_car = self.client.get(CAR_LIST_URL)
        self.car123 = Car.objects.create(
            model="Test Car123",
            manufacturer_id=1
        )
        self.car456 = Car.objects.create(
            model="Test Car456",
            manufacturer_id=2
        )

        self.response_driver = self.client.get(DRIVER_LIST_URL)
        Driver.objects.create(
            username="Test Driver123",
            password="driver123",
            license_number="ABC123123"
        )
        Driver.objects.create(
            username="Test Driver456",
            password="driver456",
            license_number="ABC456456"
        )
        self.toggle_car_assign_url = reverse(
            "taxi:toggle-car-assign",
            args=[self.car123.pk]
        )

    def test_retrive_manufacturers(self):
        self.assertEqual(self.response_manufacturer_p1.status_code, 200)
        self.assertEqual(
            self.manufacturer_2_pages,
            list(self.all_manufacturers)
        )
        self.assertTemplateUsed(
            self.response_manufacturer_p1,
            "taxi/manufacturer_list.html"
        )

    def test_manufacturer_get_context_data(self):
        self.assertIsInstance(
            self.response_manufacturer_p1.context["search_form"],
            ManufacturerSearchForm
        )

    def test_manufacturer_get_queryset_with_valid_form(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "Test"}
        )

        self.assertContains(response, "Test Manufacturer1")
        self.assertContains(response, "Test Manufacturer5")

    def test_manufacturer_get_queryset_with_invalid_form(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "InvalidName"}
        )

        self.assertNotContains(response, "Test Manufacturer1")
        self.assertNotContains(response, "Test Manufacturer7")
        self.assertContains(response, "InvalidName")

    def test_manufacturer_get_queryset_without_search_form_data(self):
        self.assertEqual(
            self.manufacturer_2_pages,
            list(self.all_manufacturers),
        )

    def test_manufacturer_pagination(self):
        self.assertEqual(self.response_manufacturer_p1.status_code, 200)

        self.assertContains(
            self.response_manufacturer_p1,
            "Test Manufacturer1"
        )
        self.assertContains(
            self.response_manufacturer_p1,
            "Test Manufacturer5"
        )
        self.assertNotContains(
            self.response_manufacturer_p1,
            "Test Manufacturer6"
        )

        self.assertContains(
            self.response_manufacturer_p2,
            "Test Manufacturer6"
        )
        self.assertContains(
            self.response_manufacturer_p2,
            "Test Manufacturer7"
        )

        self.assertIsInstance(
            self.response_manufacturer_p1.context["paginator"],
            Paginator
        )
        self.assertEqual(
            str(self.response_manufacturer_p1.context["page_obj"]),
            "<Page 1 of 2>"
        )
        self.assertTrue(self.response_manufacturer_p1.context["is_paginated"])

    def test_car_get_context_data(self):
        self.assertIsInstance(
            self.response_car.context["search_form"], CarSearchForm
        )

    def test_car_get_queryset_with_valid_form(self):
        response = self.client.get(
            CAR_LIST_URL,
            {"model": "Test Car123"}
        )
        self.assertContains(response, "Test Car123")
        self.assertNotContains(response, "Test Car456")

    def test_car_get_queryset_with_invalid_form(self):
        response = self.client.get(
            CAR_LIST_URL,
            {"model": "InvalidName"}
        )
        self.assertNotContains(response, "Test Car123")
        self.assertNotContains(response, "Test Car456")

    def test_driver_get_context_data(self):
        self.assertIsInstance(
            self.response_driver.context["search_form"], DriverSearchForm
        )

    def test_driver_get_queryset_with_valid_form(self):
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": "Test Driver123"}
        )
        self.assertContains(response, "Test Driver123")
        self.assertNotContains(response, "Test Driver456")

    def test_driver_get_queryset_with_invalid_form(self):
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": "InvalidName"}
        )
        self.assertNotContains(response, "Test Driver123")
        self.assertNotContains(response, "Test Driver456")

    def test_toggle_assign_existing_car(self):
        self.user.cars.add(self.car123)
        self.client.get(self.toggle_car_assign_url)

        self.assertNotIn(self.car123, self.user.cars.all())

    def test_toggle_assign_new_car(self):
        self.client.get(self.toggle_car_assign_url)
        self.assertIn(self.car123, self.user.cars.all())
