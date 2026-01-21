from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="Test name",
            password="password123",
            license_number="ASD12345",
        )
        self.update_url = reverse("taxi:driver-update", args=[self.driver.id])
        self.delete_url = reverse("taxi:driver-delete", args=[self.driver.id])

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1", password="password1", license_number="ADA12345"
        )
        Driver.objects.create(
            username="driver2", password="password2", license_number="ADA67890"
        )

        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "newdriver",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "license_number": "XYZ98765",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="newdriver").exists())

    def test_update_driver_view(self):
        form_data = {
            "license_number": "UPD12345",
        }
        response = self.client.post(self.update_url, data=form_data)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "UPD12345")

    def test_delete_driver(self):
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())
