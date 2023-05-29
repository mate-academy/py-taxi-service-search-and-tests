from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):

    def test_login_required(self):
        response = self.client.get(DRIVERS_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Kostya",
            password="password123",
            license_number="ABCD12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="Kostya_Test",
            password="987654321some_test",
            license_number="ABC12345"
        )
        response = self.client.get(DRIVERS_LIST_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "Kostya_Test",
            "password1": "987654321some_test",
            "password2": "987654321some_test",
            "first_name": "Kostya",
            "last_name": "Kononenko",
            "license_number": "ABC11234"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        test_user = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(test_user.first_name, form_data["first_name"])
        self.assertEqual(test_user.last_name, form_data["last_name"])
        self.assertEqual(test_user.license_number, form_data["license_number"])

    def test_driver_list_search_by_username(self):
        response = self.client.get(DRIVERS_LIST_URL, {"username": "Kostya"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username="Kostya"))
        )
