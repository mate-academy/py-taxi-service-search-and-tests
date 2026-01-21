from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="testlicense"

        )

    def test_driver_license_list_display(self):
        """
        test that driver's license number is in list_display on admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_fieldsets(self):
        """
                test that driver's additional info
                is in list_display on admin page
                :return:
                """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_add_fieldsets(self):
        """
                test that driver's additional info
                is added in list_display on admin page
                :return:
                """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, self.driver.id)
