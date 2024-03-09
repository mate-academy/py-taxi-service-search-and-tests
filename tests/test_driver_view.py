from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


URL_DRIVER_LIST = "taxi:driver-list"


class PublicDriverViewTest(TestCase):
    def test_driver_login_required(self) -> None:
        response = self.client.get(reverse(URL_DRIVER_LIST))

        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/"
        )


class PrivateDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            license_number="AAA55555"
        )

        self.client.force_login(self.user)

    def test_driver_correct_template(self) -> None:
        response = self.client.get(reverse(URL_DRIVER_LIST))

        self.assertEqual(str(response.context["user"]), "test_username ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_list(self) -> None:
        get_user_model().objects.create(
            username="Max",
            password="max123",
            license_number="AAA12345"
        )
        get_user_model().objects.create(
            username="Nick",
            password="nick123",
            license_number="AAA54321"
        )
        response = self.client.get(reverse(URL_DRIVER_LIST))
        drivers = get_user_model().objects.all()

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_driver_list_search(self) -> None:
        get_user_model().objects.create(
            username="Max",
            password="max123",
            license_number="AAA12345"
        )
        get_user_model().objects.create(
            username="Nick",
            password="nick123",
            license_number="AAA54321"
        )

        response = self.client.get(reverse(URL_DRIVER_LIST) + "?username=ax")
        driver = get_user_model().objects.filter(username="Max")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
