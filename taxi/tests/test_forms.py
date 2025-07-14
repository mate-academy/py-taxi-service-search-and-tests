from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Fiat", country="Italy")

    def test_search_form_filters_queryset(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "toyo"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "Fiat")

    def test_search_form_valid(self):
        form_data = {"name": "ford"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "ford")
