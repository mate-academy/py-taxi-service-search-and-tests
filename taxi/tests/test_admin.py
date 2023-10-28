from django.contrib.auth import get_user_model
from django.test import TestCase
from django.apps import apps
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class AdminRegisteredModelTest(TestCase):

    def test_required_registered_models(self) -> None:
        required_registered_models = [
            Car, Driver, Manufacturer
        ]

        for model in required_registered_models:
            self.assertIn(model, apps.get_models())


class DriverAdminTest(TestCase):

    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="admin.user",
            password="2345assdSS",
        )
        self.client.force_login(self.superuser)

        self.driver = get_user_model().objects.create_user(
            username="test.user",
            password="123useruser",
            license_number="ABC12345"
        )

    def test_license_number_in_driver_changelist(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.license_number)

    def test_additional_info_with_license_in_driver_change(self) -> None:
        url = reverse("admin:taxi_driver_change",
                      kwargs={"object_id": self.driver.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Additional info</h2>")
        self.assertContains(response, self.driver.license_number)

    def test_additional_info_with_fields_in_driver_add(self) -> None:
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        required_input_fields = [
            'name="first_name"',
            'name="last_name"',
            'name="license_number"'
        ]

        self.assertEqual(response.status_code, 200)

        for input_field in required_input_fields:
            self.assertContains(response, input_field)


class CarAdminTest(TestCase):

    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="admin.user",
            password="2345assdSS",
        )
        self.client.force_login(self.superuser)

    def test_search_form_in_car_changelist(self) -> None:
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="submit" value="Search">')
