from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="12345",
            license_number="ADM12345"
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test password",
            license_number="TTT12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test check driver license_number is in list_display on
        driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test check driver license_number is in display on
        driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_create_new_fieldsets_listed(self):
        """
        Test check driver first_name, last_name license_number
        is in display on driver add admin page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, 'name="first_name"')
        self.assertContains(res, 'name="last_name"')
        self.assertContains(res, 'name="license_number"')
