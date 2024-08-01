from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="passowrdtest"
        )
        self.client.force_login(self.admin_user)
        self.driver = Driver.objects.create(
            username="adminname",
            password="<PASSWORD>",
            license_number="AB25632"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number listed on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed_(self):
        """
        Test that driver's license number listed on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_info_listed_(self):
        """
        Test that driver's license number, first name, last
        name listed on driver detail add admin page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
