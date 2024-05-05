from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(BaseTestCase):
    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Ford Motor Company")
        Manufacturer.objects.create(name="BMW")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchTest(BaseTestCase):
    def test_search_by_name_manufacturers(self):
        Manufacturer.objects.create(name="Ford")
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Audi")

        response = self.client.get(MANUFACTURER_URL, {"name": "Fo"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Ford")
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Audi")

    def test_no_results_found(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "XYZ"})
        self.assertEqual(response.status_code, 200)


class PrivateDriverTests(BaseTestCase):
    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
