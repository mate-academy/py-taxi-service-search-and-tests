from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Manufacturer

MANUFACTURER_ULR = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        test_response = self.client.get(MANUFACTURER_ULR)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="manufacturer1", country="country")
        Manufacturer.objects.create(name="manufacturer2", country="country")
        test_response = self.client.get(MANUFACTURER_ULR)
        self.assertEqual(test_response.status_code, 200)
        all_manufacturers = Manufacturer.objects.all()
        self.assertEqual(all_manufacturers.count(), 2)
        self.assertTemplateUsed(test_response, "taxi/manufacturer_list.html")
