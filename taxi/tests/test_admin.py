from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model().objects.create_superuser(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user_model)
        self.author = get_user_model().objects.create_user(
            username="vas",
            password="vas12345",
            license_number="ASD12345"
        )

    def test_admin_license_number_exist(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.license_number)

    def test_admin_license_number_additional_info(self):
        url = reverse("admin:taxi_driver_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.license_number)

    def test_admin_license_number_exist_create(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")
