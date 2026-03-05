from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver
from taxi.views import DriverListView


class DriverListTest(TestCase):

    def setUp(self):
        user = Driver.objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(user)
        self.response = self.client.get(reverse("taxi:driver-list"))

    def test_get_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(DriverListView.paginate_by, 5)

    def test_get_context(self):
        self.assertIn("search", self.response.context)

    def test_search(self):
        drivers_list = [
            Driver.objects.create_user(
                username=f"username_{i}",
                password=f"password__{i}",
                license_number=f"ABC1234{i}"

            )
            for i in range(10)
        ]

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "username_1"}
        )

        drivers = response.context.get("driver_list")
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers.model, Driver)
