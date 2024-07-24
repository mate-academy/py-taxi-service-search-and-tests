from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        Manufacturer.objects.create(
            name="test1",
            country="country2"
        )
        responce = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(responce.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(responce.context["manufacturer_list"]),
            list(manufacturer)
        )


class TestManufacturerListView(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="test 2", country="test country 2")
        Manufacturer.objects.create(name="test", country="test country")
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)
        self.url = f"{MANUFACTURER_FORMAT_URL}?name=test"

    def test_view_search(self):
        responce = self.client.get(self.url)
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(len(list(responce.context["object_list"])), 2)


class CarUpdateViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            license_number="MOV12345",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)
        self.update_url = reverse("taxi:driver-update", args=[self.driver.id])

    def test_update_license_number(self):
        new_license = "POV12345"
        responce = self.client.post(
            self.update_url,
            {
                "license_number": new_license
            }
        )
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, new_license)
        self.assertEqual(responce.status_code, 302)
