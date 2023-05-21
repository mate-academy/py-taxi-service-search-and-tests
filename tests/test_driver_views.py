from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):

    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword11",
            license_number="TTT12332"

        )
        self.client.force_login(self.user)

    def test_driver_list(self):
        get_user_model().objects.create_user(
            username="testuser1",
            password="testpassword112",
            license_number="TTA12332"
        )

        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_create_driver(self):
        form_data = {
            "username": "usertest1",
            "password1": "passwordteest123",
            "password2": "passwordteest123",
            "first_name": "user",
            "last_name": "test",
            "license_number": "ADA12331"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertTrue(new_user.check_password(form_data["password1"]))

    def test_search_driver(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "usertest1"})

        self.assertTrue(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username="usertest1"))
        )
