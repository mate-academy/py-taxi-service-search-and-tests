from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="user_test",
            password="test_pass"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEquals(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_filtering_manufacturer_by_name(self):
        response = self.client.get(
            MANUFACTURER_URL,
            data={"name": self.manufacturer1.name}
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
