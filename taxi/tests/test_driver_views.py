from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver


DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.driver = Driver.objects.create(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="123456",
        )

    def setUp(self):
        self.client.login(username="testuser", password="testpass")

    def test_driver_list_view(self):
        response = self.client.get(DRIVERS_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(drivers), list(response.context["driver_list"]))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_with_search(self):
        response = self.client.get(DRIVERS_URL, {"username": "1"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")

    def test_driver_create_view(self):
        form_data = {
            "username": "driver1",
            "password1": "password",
            "password2": "password",
            "first_name": "driver",
            "last_name": "driver",
            "email": "driver@driver.com",
            "license_number": "AAA22345",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_driver_update_view(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.driver.pk}),
            {"license_number": "AAA22222"},
        )

        self.assertRedirects(response, DRIVERS_URL)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(
            get_user_model().objects.get(pk=self.driver.pk).license_number,
            "AAA22222"
        )

    def test_driver_delete_view(self):
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertFalse(
            get_user_model().objects.filter(pk=self.driver.pk).exists()
        )
