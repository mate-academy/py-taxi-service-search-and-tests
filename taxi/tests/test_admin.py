from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

Driver = get_user_model()


class DriverAdminTest(TestCase):
    def setUp(self):
        admin_user = Driver.objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(admin_user)
        self.driver = Driver.objects.create_user(
            username="author",
            password="testauthor",
            license_number="AAA12345"
        )

    def test_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_detail_has_license_number_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        response = self.client.get(url)
        self.assertContains(
            response,
            self.driver.license_number
        )

    def test_add_has_additional_info_fieldset(self):
        url = reverse(
            "admin:taxi_driver_add",
        )
        response = self.client.get(url)

        self.assertContains(
            response,
            "Additional info"
        )
        self.assertContains(
            response,
            'name="first_name"'
        )
        self.assertContains(
            response,
            'name="last_name"'
        )
        self.assertContains(
            response,
            'name="license_number"'
        )
