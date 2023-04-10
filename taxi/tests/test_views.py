from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

    def test_get_context_data(self):
        url = "/manufacturers/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )

    def test_get_queryset_filtered(self):
        url = "/manufacturers/?name=Toy"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            [self.manufacturer1]
        )

    def test_get_queryset_not_filtered(self):
        url = "/manufacturers/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            [self.manufacturer1, self.manufacturer2],
            ordered=False
        )
