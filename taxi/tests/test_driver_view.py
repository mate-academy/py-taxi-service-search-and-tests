from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test username",
            password="Pass1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_retrieve_all_drivers(self):
        get_user_model().objects.create(
            username="Test username 1",
            password="Pass1234",
            license_number="CDE12345",
        )
        get_user_model().objects.create(
            username="Test username 2",
            password="Pass1234",
            license_number="BCD23456",
        )

        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_name",
            "password1": "User12345",
            "password2": "User12345",
            "first_name": "Userfirst",
            "last_name": "Userlast",
            "license_number": "ZZZ11111"
        }
        self.client.post(DRIVER_CREATE_URL, form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_search_driver(self):
        get_user_model().objects.create(
            username="username1",
            password="Pass1234",
            license_number="ABC33333",
        )
        get_user_model().objects.create(
            username="username2",
            password="Pass1234",
            license_number="BCD44444",
        )
        get_user_model().objects.create(
            username="drivername",
            password="Pass1234",
            license_number="BCD55555",
        )
        res = self.client.get(DRIVER_LIST_URL, {"username": "user"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "username1")
        self.assertContains(res, "username2")
        self.assertNotContains(res, "drivername")


class DriverLicenseNumberUpdateTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="john.fast",
            password="1qazcde3",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)
        self.url = reverse("taxi:driver-update", kwargs={"pk": self.driver.pk})

    def test_update_license_number(self):
        new_license_number = "NEW12345"
        res = self.client.post(
            self.url,
            {"license_number": new_license_number}
        )
        self.driver.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.driver.license_number, new_license_number)
