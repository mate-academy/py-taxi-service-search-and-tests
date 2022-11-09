from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):
    def test_login_required_list(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateLiteraryFormatTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="billy.hargrove",
            password="pro12345",
            first_name="Billy",
            last_name="Hargrove",
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="FCA",
            country="Italy",
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="some.user",
            password="pro12345",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "jim.hopper",
            "password1": "bobo765",
            "password2": "bobo765",
            "license_number": "JIM26531",
            "first_name": "Jim",
            "last_name": "Hopper",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"],
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
