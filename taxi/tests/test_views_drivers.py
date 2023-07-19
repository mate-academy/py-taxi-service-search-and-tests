from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class DriverPublicTest(TestCase):

    def test_car_list_logout(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2Fdrivers%2F")

    def test_car_detail(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
            license_number="TES12345"
        )

        url = reverse("taxi:car-detail", kwargs={"pk": driver.id})
        response = self.client.get(url)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2Fcars%2F1%2F")


class DriverTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3"
        )
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create(
            username="test_driver",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
            license_number="TES12345"
        )

    def test_update_driver(self):
        url = reverse("taxi:driver-update", kwargs={"pk": self.driver.id})
        test_license_number = "TES12345"

        data = {"license_number": test_license_number}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

    def test_driver_delete(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": self.driver.id})

        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=self.driver.id).exists()
        )
