from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_superuser(
            username="driver",
            email="<EMAIL>",
            password="<PASSWORD>",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_driver_listed(self):
        """
        Test that driver's license number is in list_display on
        driver's admin page.
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
