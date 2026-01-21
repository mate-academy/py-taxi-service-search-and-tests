from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.tests.test_views.initial_data import (
    MANUFACTURER_DATA,
    MANUFACTURER_URLS
)
from taxi.models import Manufacturer


class ManufacturerChangesViewTest(TestCase):
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

        self.client.force_login(self.user)

    def test_successful_manufacturer_creation(self):
        response = self.client.post(
            MANUFACTURER_URLS["test_manufacturer_create_url"],
            data=MANUFACTURER_DATA
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Manufacturer.objects.filter(name="test_name1").exists()
        )
        self.assertRedirects(
            response,
            MANUFACTURER_URLS["test_manufacturer_list_url"]
        )

    def test_unsuccessful_manufacturer_creation(self):
        data = {"name": "test"}
        response = self.client.post(
            MANUFACTURER_URLS["test_manufacturer_create_url"],
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Manufacturer.objects.filter(name="test").exists()
        )

    def test_manufacturer_update_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.pk}
            ),
            data=MANUFACTURER_DATA
        )
        self.assertRedirects(
            response,
            MANUFACTURER_URLS["test_manufacturer_list_url"]
        )

    def test_manufacturer_successful_deletion_redirects_to_success_url(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer.pk}
            )
        )
        self.assertRedirects(response,
                             MANUFACTURER_URLS["test_manufacturer_list_url"]
                             )

    def test_successful_deletion_removes_manufacturer_from_database(self):
        self.client.post(MANUFACTURER_URLS["test_manufacturer_delete_url"])
        self.assertFalse(Manufacturer.objects.filter(
            pk=self.manufacturer.pk
        ).exists())
