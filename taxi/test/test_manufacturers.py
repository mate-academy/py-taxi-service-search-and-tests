from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer
from django.contrib.auth import get_user_model

User = get_user_model()


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="BMWoto")
        Manufacturer.objects.create(name="Audi")
        user = User.objects.create_user(
            username="peter", password="test1234", license_number="HTY1234"
        )
        self.client.force_login(user)

    def test_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        resp = self.client.get(url, {"name": "BMW"})
        self.assertEqual(resp.status_code, 200)
        qs = resp.context.get("manufacturer_list")
        self.assertEqual(len(qs), 2)
        names = [m.name for m in qs]
        self.assertIn("BMW", names)
        self.assertIn("BMWoto", names)
