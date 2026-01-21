from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car
from taxi.tests.test_views.initial_data import (
    CAR_URLS,
    CAR_TEMPLATES_PATH
)


class PublicCarURLsTest(TestCase):
    def test_manufacturer_view_login_required(self):
        for test_name, url in CAR_URLS.items():
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)


class PrivateCarURLsAndTemplatesTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.car.drivers.add(self.user)

        self.client.force_login(self.user)

    def test_car_view_correct_url_login_completed(self):
        for test_name, url in CAR_URLS.items():
            with self.subTest(test_name, url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_car_view_correct_template_login_completed(self):
        for url, template_path in CAR_TEMPLATES_PATH.items():
            with self.subTest(f"test_{template_path}"):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template_path)
