from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class LoggedInTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )

    def setUp(self):
        self.client.force_login(self.user1)


class DriverListSearchTests(LoggedInTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user2 = get_user_model().objects.create_user(
            username="john.doe",
            license_number="JOH12345",
            first_name="John",
            last_name="Doe",
            password="1qazcde3",
        )

    def test_search_empty_query(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john.doe"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "nonexistent"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no drivers in the service.",
        )


class CarModelSearchTests(LoggedInTestCase):
    def setUp(self) -> None:
        super().setUp()
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.car1 = Car.objects.create(
            model="Model X",
            manufacturer=manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Model Y",
            manufacturer=manufacturer,
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Model X"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.car1))
        self.assertNotContains(response, str(self.car2))

    def test_search_empty_query(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.car1))
        self.assertContains(response, str(self.car2))
