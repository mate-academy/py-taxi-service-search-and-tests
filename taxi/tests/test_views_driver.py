from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTest(TestCase):
    def test_login_list_required(self):
        result_list = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(result_list.status_code, 200)

    def test_login_create_required(self):
        result_create = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEqual(result_create.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "test_name_username",
            "test_password"
        )
        self.client.force_login(self.driver)

    def test_login_create_required(self):
        Driver.objects.create(
            license_number="AX-895-WE",
        )
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html")

    def test_login_update_required(self):
        driver = Driver.objects.create(
            license_number="AX-895-WE",
        )
        url = reverse("taxi:driver-update", args=[driver.pk])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
