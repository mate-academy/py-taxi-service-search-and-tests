from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class ViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            license_number="12345678")
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123")
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany")

    def test_manufacturer_list(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"
        ))
        self.assertEquals(
            response.context["search_form"],
            ManufacturerSearchForm)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()))
