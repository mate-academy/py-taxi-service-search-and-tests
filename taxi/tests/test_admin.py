import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        unique_license_number = str(uuid.uuid4())[:8]

        self.driver = get_user_model()(
            username="driver",
            license_number=unique_license_number,
        )
        self.driver.set_password("testdriver")

        self.driver.save()

    def test_driver_list_page_contains_license_number(self):

        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_page_contains_all_fields(self):

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.driver.license_number)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
