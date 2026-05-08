from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test123",
            license_number="TST12345"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create_user(
            username="User",
            password="UserPassword",
            license_number="USE12345"
        )

    def test_retrieve_drivers(self):
        Driver.objects.create_user(
            username="Test1",
            password="TestPassword1",
            license_number="TST22345"
        )
        Driver.objects.create_user(
            username="Test2",
            password="TestPassword2",
            license_number="TST32345"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_filters_queryset(self):
        username = "Test1"
        response = self.client.get(DRIVER_URL, {"username": username})

        self.assertEqual(response.status_code, 200)

        expected = Driver.objects.filter(username__icontains=username)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(expected)
        )

    def test_search_empty_returns_all(self):
        response = self.client.get(DRIVER_URL, {"name": ""})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all())
        )

    def test_create_driver(self):
        form_data = {
            "username": "TestUsername111",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
            "license_number": "AAA12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = Driver.objects.get(username=form_data["username"])

        self.assertEqual(new_driver.username, form_data["username"])
        self.assertTrue(new_driver.check_password(form_data["password1"]))
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_update_driver_license_number(self):
        form_data = {
            "license_number": "NEW12345"
        }
        self.client.post(reverse(
            "taxi:driver-update",
            args=[self.driver.id]
        ), data=form_data)
        self.driver.refresh_from_db()

        self.assertEqual(
            self.driver.license_number,
            form_data["license_number"]
        )

    def test_confirm_delete_driver(self):
        response = self.client.get(
            reverse(
                "taxi:driver-delete",
                args=[self.driver.id]
            ), follow=True
        )
        self.assertContains(response, "Delete driver?")

    def test_delete_driver(self):
        post_response = self.client.post(
            reverse(
                "taxi:driver-delete",
                args=[self.driver.id]
            ), follow=True
        )
        self.assertRedirects(post_response, reverse("taxi:driver-list"))
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())
