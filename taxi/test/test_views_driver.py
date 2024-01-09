from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(
            res,
            "taxi/driver_list.html"
        )

    def test_search_cars(self):
        res = self.client.get(DRIVER_URL + "?username=test")
        driver = get_user_model().objects.filter(username__icontains="test")
        self.assertEqual(
            list(res.context["driver_list"]),
            list(driver)
        )

    def test_create_drivers(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "new_username",
                "password1": "new_password",
                "password2": "new_password",
                "license_number": "ABC12345",
                "first_name": "John",
                "last_name": "Doe",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="new_username").exists()
        )

    def test_update_driver(self):
        res = self.client.post(
            reverse("taxi:driver-update", args=[1]),
            {
                "license_number": "ABC12346",
            }
        )
        self.assertRedirects(res, reverse("taxi:driver-list"))
        self.assertTrue(
            get_user_model().objects.filter(license_number="ABC12346").exists()
        )

    def test_delete_driver(self):
        response = self.client.post(
            reverse(
                "taxi:driver-delete",
                args=[1]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=1).exists()
        )
