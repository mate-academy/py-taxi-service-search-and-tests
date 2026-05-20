from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class PublicDriverTests(TestCase):
    def test_login_required(self):
        """Test that login is required for views"""
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="12345",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

    def test_retriever_driver_list(self):
        """Test that retriever driver list is working"""
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)

    def test_search_driver_by_username(self):
        """Test that search driver by username is working"""
        get_user_model().objects.create_user(
            username="john_driver",
            password="12345",
            license_number="ABC12545"
        )
        get_user_model().objects.create_user(
            username="mike_driver",
            password="12345",
            license_number="ABC12345"
        )
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"}
        )
        self.assertContains(res, "john_driver")
        self.assertNotContains(res, "mike_driver")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="12345",
            license_number="TEST12345"
        )

        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_search_car_by_model(self):
        """Test that search car by model is working"""
        Car.objects.create(
            model="Tesla",
            manufacturer=self.manufacturer,
        )

        Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer,
        )

        res = self.client.get(reverse("taxi:car-list"), {"search": "Tesla"})
        self.assertContains(res, "Tesla")
        self.assertNotContains(res, "BMW X5")


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="12345",
            license_number="TEST12345"
        )

        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Toy"}
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
