from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Driver, Manufacturer


class ViewTestSetupMixin:
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password12345"
        )
        self.client.force_login(self.user)


class CarListViewTest(ViewTestSetupMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cars = 13
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Test Model {car_id}",
                manufacturer=manufacturer,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)


class DriverListViewTest(ViewTestSetupMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 13
        for driver_id in range(number_of_drivers):
            Driver.objects.create_user(
                username=f"testdriver{driver_id}",
                password="password12345",
                license_number=f"ABC123{driver_id}",
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)

    def test_lists_all_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)


class ManufacturerListViewTest(ViewTestSetupMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 13
        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(name=f"Manufacturer {manufacturer_id}")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)


class SearchFeatureTest(ViewTestSetupMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        cls.car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )
        cls.driver = Driver.objects.create_user(
            username="testdriver",
            password="password12345",
            license_number="ABC12345"
        )

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Test"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Test"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
