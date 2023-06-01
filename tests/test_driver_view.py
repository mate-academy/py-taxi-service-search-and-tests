from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345"
        }

        self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_deliver_lisr(self):
        get_user_model().objects.create_user(
            username="test_name",
            password="password123",
            license_number="TST12345"
        )
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_search(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username="test"))
        )
