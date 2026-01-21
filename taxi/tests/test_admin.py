from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin")
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_superuser(
            username="author",
            password="testauthor",
            license_number="AAA12345",)

    def test_author_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.license_number)

    def test_author_detail_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.license_number)

    def test_additional_fields_in_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.first_name)
        self.assertContains(res, self.author.last_name)
        self.assertContains(res, self.author.license_number)
