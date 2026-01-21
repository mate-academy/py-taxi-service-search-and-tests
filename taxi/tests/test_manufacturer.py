from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required_list_page(self):
        resp = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="testpassword12345",
            license_number="ADR12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_list_page_with_search_field(self):
        Manufacturer.objects.create(name="test 1", country="country 1")
        Manufacturer.objects.create(name="test 2", country="country 2")

        resp = self.client.get(MANUFACTURERS_LIST_URL)

        manufacturers = Manufacturer.objects.all()
        form = ManufacturerSearchForm()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertEqual(
            resp.context["manufacturer_search_form"].is_valid(),
            form.is_valid()
        )
