import uuid
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        unique_suffix = uuid.uuid4().hex[:6]
        self.admin_username = f"admin_{unique_suffix}"
        self.driver_username = f"driver_{unique_suffix}"
        self.license_number = f"LIC{unique_suffix.upper()}"

        self.admin_user = get_user_model().objects.create_superuser(
            username=self.admin_username,
            password="admin"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username=self.driver_username,
            first_name="Con",
            last_name="Chen",
            password="driver1234567890!@#$%^&*()_+-={}[]|\\:;'\"<>,.?/",
            license_number=self.license_number
        )

    def test_driver_license_number_listed(self):
        """
        Test driver's license number is listed on admin page.
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test driver's license number appears on detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_add(self):
        """
        Test license number input is present on driver detail page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, 'name="license_number"')
