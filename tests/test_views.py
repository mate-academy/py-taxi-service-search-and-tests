from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="nova",
            password="nova123456",
            license_number="ASD12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Mazda", country="Japan")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_filter(self):
        Manufacturer.objects.create(name="Mazda", country="Japan")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_URL, {"name": "Audi"})
        manufacturers = Manufacturer.objects.filter(name__icontains="Audi")

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertListEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PublicDriverTests(TestCase):
    def test_login_required_for_create_new_driver(self):
        response = self.client.get(DRIVER_CREATE_URL)

        self.assertEquals(response.status_code, 302)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456",
            license_number="QQQ12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "license_number": "ASD12345",
            "first_name": "Sarah",
            "last_name": "Kerigan",
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEquals(new_driver.first_name, form_data["first_name"])
        self.assertEquals(new_driver.last_name, form_data["last_name"])
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )
