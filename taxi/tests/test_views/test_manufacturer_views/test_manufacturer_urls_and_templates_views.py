from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer
from taxi.tests.test_views.initial_data import (
    MANUFACTURER_URLS,
    MANUFACTURER_TEMPLATES_PATH
)


class PublicManufacturerURLsTest(TestCase):
    def test_manufacturer_view_login_required(self):
        for test_name, url in MANUFACTURER_URLS.items():
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerURLsAndTemplatesTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(
            name="test",
            country="test",
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="test_license",
            password="test1234",
        )

        self.client.force_login(self.user)

    def test_manufacturer_view_correct_url_login_completed(self):
        for test_name, url in MANUFACTURER_URLS.items():
            with self.subTest(test_name, url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_manufacturer_view_correct_template_login_completed(self):
        for url, template_path in MANUFACTURER_TEMPLATES_PATH.items():
            with self.subTest(f"test_{template_path}"):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template_path)
