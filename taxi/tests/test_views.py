from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublickManufacurerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_requierd(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacurerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="helloworld",
            license_number="ABC3BC"
        )
        self.client.force_login(self.user)

    def test_retrive_manufacturers(self):
        Manufacturer.objects.create(name="test123", country="123test")
        Manufacturer.objects.create(name="World", country="Hello")
        manufacturers = Manufacturer.objects.all()
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEquals(list(res.context["manufacturer_list"]),
                          list(manufacturers))

    def test_login_requierd(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEquals(res.status_code, 200)
