from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test1234"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test4321",
            license_number="test_license"
        )

    def test_driver_has_license_number(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_has_license_number_in_detail(self) -> None:
        url = reverse(
            "admin:taxi_driver_change",
            args=(self.driver.id,)
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
