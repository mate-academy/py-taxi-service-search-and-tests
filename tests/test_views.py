from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

LITERARY_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(LITERARY_FORMAT_URL)
        self.assertEqual(res.status_code, 302)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test2",
            password="test1456",
        )
        self.client.force_login(self.user)

    def test_create_driver(self) -> None:
        form_data = {
            "username": "new_user",
            "password1": "usertest174",
            "password2": "usertest174",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
