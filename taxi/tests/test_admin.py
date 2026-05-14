from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.adminUser = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )

        self.client.force_login(self.adminUser)

        username = "test"
        first_name = "test"
        last_name = "test"
        license_number = "RFE12345"
        password = "abdhf1234"

        self.driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            password=password,
            last_name=last_name,
            license_number=license_number
        )

    def test_driver_license_number_in_list(self):
        """test driver if license number of driver is in list
        :return
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail(self):
        """test if license number of driver is in detail page list
        :return
        """
        url = reverse("admin:taxi_driver_change",
                      args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
