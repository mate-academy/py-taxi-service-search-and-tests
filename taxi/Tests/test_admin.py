from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test_admin"
        )
        self.client.force_login(admin_user)
        self.driver = User.objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number",
        )

    def test_driver_license_number(self):
        """
        Test driver License number
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number(self):
        """
        Test driver License number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
