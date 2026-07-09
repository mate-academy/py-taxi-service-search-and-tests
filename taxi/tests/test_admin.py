from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="testadmin",
            first_name="first",
            last_name="last",
            email="admin@test.com",
            password="test123test",
            license_number="QWE12345",
        )
        self.client.force_login(self.user)

    def test_driver_admin_list(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.license_number)

    def test_driver_fieldset(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.pk])
        res = self.client.get(url)
        self.assertContains(res, self.user.license_number)

    def test_driver_add_fieldset(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "License number")
