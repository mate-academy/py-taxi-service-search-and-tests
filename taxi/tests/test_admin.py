from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234",
            license_number="AAA12345"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="user1234",
            license_number="BBB6789"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        resp = self.client.get(url)

        self.assertContains(resp, self.driver.license_number)

    def test_driver_license_number_detailed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        resp = self.client.get(url)

        self.assertContains(resp, self.driver.license_number)

    def test_add_fields_are_listed(self):
        url = reverse("admin:taxi_driver_add")
        resp = self.client.get(url)
        # with open("resp.html", "w") as f:
        #     f.write(str(resp.content))

        self.assertContains(resp, "First name")
        self.assertContains(resp, "Last name")
        self.assertContains(resp, "License number")
