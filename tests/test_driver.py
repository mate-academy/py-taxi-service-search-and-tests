from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver
from django.contrib.auth import get_user_model


class DriverTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user", email="test@example.com", password="password123"
        )
        self.client.login(username="user", password="password123")

    def test_create_driver(self):
        form_data = {
            "username": "newdriver",
            "password1": "Password123!",
            "password2": "Password123!",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Driver.objects.filter(username="newdriver").exists()
        )

    def test_update_license_valid_data(self):
        driver = Driver.objects.create(
            username="driver1", license_number="ABC12345"
        )
        form_data = {"license_number": "VVV77799"}
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": driver.pk}),
            data=form_data
        )
        driver.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(driver.license_number, "VVV77799")

    def test_update_driver_license_number_invalid_data(self):
        test_license_number = "7777AA"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)

    def test_search_driver(self):
        Driver.objects.create(username="driver1", license_number="ABC12345")
        Driver.objects.create(username="driver2", license_number="QWE12345")
        response = self.client.get(reverse("taxi:driver-list") + "?q=driver1")
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")
