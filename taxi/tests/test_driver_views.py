from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTest(TestCase):
    def test_login_required_driver_list(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="test123user",
        )
        Driver.objects.create(
            username="Andriy",
            password="<PASSWORD>",
            license_number="ASD84321"
        )
        Driver.objects.create(
            username="Oleh",
            password="<PASSWORD>",
            license_number="ZOV84321"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed("taxi/driver_list.html")

    def test_get_context_data_driver(self):
        response = self.client.get(DRIVER_URL, {"username": "test user"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["username"], self.user.username)

    def test_get_queryset_driver(self):
        response = self.client.get(DRIVER_URL, {"username": "andr"})
        driver_usernames = [
            driver.username
            for driver in response.context["driver_list"]
        ]
        self.assertIn("Andriy", driver_usernames)
        self.assertNotIn("Oleh", driver_usernames)
        self.assertNotIn("test user", driver_usernames)


class PrivateDriverCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_create_driver(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_driver(self):
        form_data = {
            "username": "Andriy",
            "license_number": "ASH84321",
            "password1": "pass123word098test",
            "password2": "pass123word098test",
        }
        response = self.client.post(DRIVER_CREATE_URL, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="Andriy").exists())


class PrivateDriverUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Andriy",
            license_number="ASD84321",
            password="<PASSWORD>",
        )
        self.url = reverse("taxi:driver-update", args=[self.user.id])
        self.client.force_login(self.user)

    def test_retrieve_update_driver(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_update_driver(self):
        form_data = {
            "license_number": "NAB30473",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Driver.objects.filter(license_number="NAB30473").exists()
        )


class PrivateDriverDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Andriy",
            license_number="ASD84321",
            password="<PASSWORD>",
        )
        self.driver = Driver.objects.create(
            username="Oleh",
            license_number="ZOV84321",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-delete", args=[self.driver.id])

    def test_retrieve_delete_driver(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_delete_driver(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Driver.objects.filter(username="Oleh").exists())
