from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="admin",
            password="admin1234",
            license_number="HTD65497"
        )

        self.client.force_login(self.driver)

    def test_create_driver(self):
        user_data = {
            "username": "test_user",
            "password1": "test1234test",
            "password2": "test1234test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=user_data)

        test_user = get_user_model().objects.get(
            username=user_data["username"]
        )

        self.assertEqual(test_user.first_name, user_data["first_name"])
        self.assertEqual(test_user.last_name, user_data["last_name"])
        self.assertEqual(test_user.license_number, user_data["license_number"])
