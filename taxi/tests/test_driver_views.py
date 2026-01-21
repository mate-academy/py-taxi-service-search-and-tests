from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver


DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="test_username1",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="test_username2",
            license_number="CBA54321"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username_returns_correct_results(self):
        Driver.objects.create(
            username="test_username",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="otheruser",
            license_number="CBA54321"
        )
        response = self.client.get(DRIVER_URL, {"username": "test_usern"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_username")
        self.assertNotContains(response, "otheruser")

    def test_search_driver_by_username_no_match(self):
        Driver.objects.create(
            username="test_username",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="otheruser",
            license_number="CBA54321"
        )
        response = self.client.get(DRIVER_URL, {"username": "anotheuther"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "test_username")
        self.assertNotContains(response, "otheruser")
        self.assertEqual(
            list(response.context["driver_list"]),
            []
        )

    def test_search_driver_without_query_returns_all(self):
        Driver.objects.create(
            username="test_username",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="otheruser",
            license_number="CBA54321"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_username")
        self.assertContains(response, "otheruser")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "CBA54321",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
