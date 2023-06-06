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
            username="Test_name",
            password="test_pass1234",
            license_number="QWE12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="Test_name1",
            password="test_pass1234",
            license_number="QWE12355"
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
            "username": "Test_name1",
            "password1": "test_pass1234",
            "password2": "test_pass1234",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "QWE12355"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        test_user = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(test_user.first_name, form_data["first_name"])
        self.assertEqual(test_user.last_name, form_data["last_name"])
        self.assertEqual(test_user.license_number, form_data["license_number"])

    def test_driver_list_search_by_username(self):
        response = self.client.get(DRIVERS_LIST_URL, {"username": "Test_name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username="Test_name"))
        )
