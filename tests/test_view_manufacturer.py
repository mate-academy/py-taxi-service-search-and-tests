from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="testuser",
            password="<PASSWORD>",
        )
        Manufacturer.objects.create(name="BMW", country="US")
        Manufacturer.objects.create(name="Mercedes-Benz", country="DE")
        Manufacturer.objects.create(name="Audi", country="FR")

    def setUp(self):
        self.client.force_login(self.user)

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_context(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn("search_form", response.context)

    def test_list_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertContains(response, "Mercedes-Benz")
        self.assertContains(response, "Audi")

    def test_list_manufacturer_search_by_name(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "mer"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "BMW")
        self.assertContains(response, "Mercedes-Benz")
        self.assertNotContains(response, "Audi")

    def test_search_with_no_match(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "toy"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Mercedes-Benz")
        self.assertNotContains(response, "Audi")
        self.assertContains(response,
                            "There are no manufacturers in the service.",
                            html=True)
