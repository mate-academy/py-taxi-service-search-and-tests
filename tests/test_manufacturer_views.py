from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURERS_LIST = reverse("taxi:manufacturer-list")


class PublicManufacturerViewListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Honda", country="Japan")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_LIST)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_view_search(self):
        """
        Search for manufacturers with the name 'Toyota'
        Verify that the search form is present in the context
        Verify that the filtered manufacturers are present in the context
        """
        form_data = {
            "name": "Toyota",
        }
        response = self.client.get(
            reverse("taxi:manufacturer-list"), data=form_data
        )
        self.assertEqual(response.status_code, 200)

        form = response.context["search_form"]
        self.assertIsInstance(form, ManufacturerSearchForm)

        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturer_list), 1)
        self.assertEqual(manufacturer_list[0].name, "Toyota")
