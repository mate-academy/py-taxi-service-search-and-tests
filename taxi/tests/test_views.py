from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

CAR_URL = reverse("taxi:car-list")

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Porsche")
        Manufacturer.objects.create(name="Ferrari")

        response = self.client.get(MANUFACTURER_URL)
        names = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(names)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
