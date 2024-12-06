from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer


class ManufacturerListViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="password123"
        )
        self.client.login(username="admin", password="password123")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)
