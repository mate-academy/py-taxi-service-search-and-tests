from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
        )
        Manufacturer.objects.create(
            name="Test_1",
        )
        Manufacturer.objects.create(
            name="Test_2",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_form(self):
        form_data = {"name": "Test_1"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_username_search(self):
        form_data = {"name": "Test_2"}
        res = self.client.get(MANUFACTURER_URL, data=form_data)
        self.assertContains(res, form_data["name"])
        self.assertNotContains(res, "12345")
