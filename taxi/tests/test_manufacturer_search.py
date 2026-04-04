from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser1",
        )
        self.client.force_login(self.user)

    def test_search_manufacturers_by_name(self):
        Manufacturer.objects.create(name="test", country="US")
        Manufacturer.objects.create(name="other", country="US")
        Manufacturer.objects.create(name="another test", country="JP")
        res = self.client.get(reverse("taxi:manufacturer-list") + "?name=test")
        self.assertEqual(res.status_code, 200)
        manufacturers = list(res.context["manufacturer_list"])
        self.assertEqual(len(manufacturers), 2)
        self.assertEqual(
            {m.name for m in manufacturers},
            {"test", "another test"}
        )
