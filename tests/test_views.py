from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEquals(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Mazda")

        res = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="max_big",
            password="admin1.admin1",
        )

        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "max_x",
            "first_name": "max",
            "last_name": "x",
            "password1": "max_x.max_x",
            "password2": "max_x.max_x",
            "license_number": "AVD12346",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
