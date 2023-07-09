from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateDriverListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "johndoe",
            "password1": "john_doe!12345",
            "password2": "john_doe!12345",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12346"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEquals(new_driver.first_name, form_data["first_name"])
        self.assertEquals(new_driver.last_name, form_data["last_name"])
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )
