from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class FromTest(TestCase):
    def test_manufacturer_search_form(self):
        form_data = {
            "name": "Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_create_form(self):
        user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(user=user)
        form_data = {
            "name": "Manufacturer",
            "country": "USA",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        self.assertEqual(len(Manufacturer.objects.all()), 1)
        manufacturer = Manufacturer.objects.get(name="Manufacturer")
        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])
