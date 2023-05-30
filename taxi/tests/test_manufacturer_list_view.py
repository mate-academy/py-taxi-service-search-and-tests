from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class TestManufacturerListView(TestCase):
    def setUp(self):
        self.client = Client
        Manufacturer.objects.create(name="volvo", country="test_country")
        Manufacturer.objects.create(name="BMW", country="test_country")
        Manufacturer.objects.create(name="Toyota", country="test_country")
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )

    def test_search_field(self):
        self.client.force_login(self.user)
        get_value = "To"
        url = reverse("taxi:manufacturer-list") + f"?name={get_value}"
        response = self.client.get(url)
        manufacturer_query = Manufacturer.objects.filter(
            name__icontains=get_value)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_query)
        )

    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertNotEquals(response.status_code, 200)
