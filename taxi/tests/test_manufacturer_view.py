from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerViewTest(TestCase):
    def test_login_required(self):
        """
        Test that login is required to access the manufacturer page
        """
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        """
        Test that login is required to access the manufacturer page
        """
        Manufacturer.objects.create(name="test_name_1",
                                    country="test_country_1")
        Manufacturer.objects.create(name="test_name_2",
                                    country="test_country_2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )
