from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm, ManufacturerNameSearchForm
from taxi.models import Manufacturer
from taxi.urls import app_name


class ModelTests(TestCase):

    def test_manufacturer_string(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer Test", country="Testland"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class AdminTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)

    def test_admin_taxi_groups(self):
        url = reverse("admin:app_list", args=[app_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        models = ["Manufacturer", "Driver", "Car"]
        for model in models:
            self.assertContains(response, f"{model}")


class LoginTests(TestCase):
    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class ViewTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="user", password="user1234"
        )
        self.client.force_login(user)

    def test_empty_list_view(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertContains(
            response,
            "There are no manufacturers in the service."
        )

    def test_filled_list_view(self):
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Testland"
        )
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertContains(response, "Test Manufacturer")


class FormTests(TestCase):

    def test_driver_license_update_form_correct_type(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_incorrect_type(self):
        form_data = {
            "license_number": "abc123456",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class SearchTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="user", password="user1234"
        )
        self.client.force_login(user)

        Manufacturer.objects.bulk_create(
            [
                Manufacturer(pk=1, name="AAA", country="Testland"),
                Manufacturer(pk=2, name="BBB", country="Testland"),
                Manufacturer(pk=3, name="CCC", country="Testland"),
            ]
        )

    def test_search_exists(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "AAA"})
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AAA")
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
