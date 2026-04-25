from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(
            username="driver1",
            password="test123",
            license_number="USR11111",
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="test123",
            license_number="USR22222",
        )
        get_user_model().objects.create_user(
            username="driver3",
            password="test123",
            license_number="USR33333",
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TES12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search_with_results(self):
        query_params = {"username": "1"}
        response = self.client.get(DRIVER_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers.filter(username__icontains=query_params["username"]))
        )

    def test_driver_search_without_results(self):
        query_params = {"username": "No results"}
        response = self.client.get(DRIVER_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            []
        )

    def test_driver_create_successful(self):
        response = self.client.post(
            DRIVER_CREATE_URL,
            data={
                "username": "driver.test",
                "password1": "qwebfhmtu775f",
                "password2": "qwebfhmtu775f",
                "first_name": "Test Name",
                "last_name": "Test Last Name",
                "license_number": "ABC12345",
            }
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_driver_create_invalid_licence_number(self):
        response = self.client.post(
            DRIVER_CREATE_URL,
            data={
                "username": "driver1.test",
                "password1": "qwebfhmtu775f",
                "password2": "qwebfhmtu775f",
                "first_name": "Test Name",
                "last_name": "Test Last Name",
                "license_number": "bv1234",
            }
        )
        self.assertEqual(response.status_code, 200)
