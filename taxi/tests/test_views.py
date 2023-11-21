from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="sakhaline",
            password="54321gfdsa"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="BAIC",
            country="China",
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search(self):
        Manufacturer.objects.create(name="BAIC", country="China")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            MANUFACTURERS_URL, data={"search_keyword": "B"}
        )

        manufacturer = Manufacturer.objects.filter(name__icontains="b")

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )

