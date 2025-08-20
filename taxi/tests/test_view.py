from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BWM", country="Germany")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_filter_manufacturer_by_name_matching(self):
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        honda = Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_URL, {"name": "ford"})
        self.assertContains(response, ford.name)
        self.assertNotContains(response, honda.name)

    def test_filter_manufacturer_by_name_non_matching(self):
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(MANUFACTURER_URL, {"name": "zzz"})
        self.assertNotContains(response, "Ford")
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_filter_manufacturer_by_name_empty(self):
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        honda = Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_URL)
        self.assertContains(response, ford.name)
        self.assertContains(response, honda.name)
