from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer, Driver
from taxi.views import ManufacturerListView, DriverListView

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
        self.factory = RequestFactory()

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="test_username_first",
            password="90Test1234",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="test_username_second",
            password="90Test1234",
            license_number="SET12345"
        )
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_create_driver(self):
        driver_data = {
            "username": "test_username_first",
            "password1": "90Test1234",
            "password2": "90Test1234",
            "license_number": "TES12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }
        res = self.client.post(reverse("taxi:driver-create"), driver_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertRedirects(res, "/drivers/2/")

    def test_update_driver_license(self):
        driver = get_user_model().objects.create_user(
            username="test_username_first",
            password="90Test1234",
            license_number="TES12345",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        driver_update = {
            "license_number": "NEW12345",
        }
        res = self.client.post(
            reverse("taxi:driver-update",
                    args=[driver.pk]),
            driver_update
        )
        self.assertEqual(res.status_code, 302)
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "NEW12345")
        self.assertRedirects(res, "/drivers/")

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="test_username_first",
            password="90Test1234",
            license_number="TES12345",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        res = self.client.post(reverse("taxi:driver-delete", args=[driver.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertRedirects(res, "/drivers/")

    def test_get_context_data_driver(self):
        get_user_model().objects.create_user(
            username="test_username_first",
            password="90Test1234",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="test_username_second",
            password="90Test1234",
            license_number="SET12345"
        )
        request = self.factory.get(
            reverse("taxi:driver-list"),
            {"username": "test_username_second"}
        )
        request.user = self.user

        view = DriverListView()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().username, "test_username_second")
