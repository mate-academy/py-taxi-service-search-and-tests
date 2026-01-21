from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="1234"
        )
        self.client.force_login(self.admin_user)
        self.driver = Driver.objects.create_user(
            username="test2",
            password="1234",
            license_number="QWE12345"
        )

    def test_driver_add_fieldsets(self):
        """
        Test the admin add page to ensure that the fields
        defined in the 'add_fieldsets' attribute
        of the admin class are displayed correctly.
        """
        url = reverse("admin:taxi_driver_add")
        resp = self.client.get(url)
        self.assertContains(resp, "license_number")
