import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="bob",
            password="ccc123",
            license_number="CCC12345"
        )
        self.client.force_login(user)

        num_of_drivers = 7
        for i in range(num_of_drivers):
            get_user_model().objects.create_user(
                username=f"{random.randint(1, 1000000)}",
                password=f"{random.randint(1, 1000)}",
                license_number=f"CCC2356{i}"
            )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertTrue("driver_list" in response.context)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers[:5])
        )

    def test_pagination_is_five(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_valid_search(self):
        get_user_model().objects.create(username="alex", password="123")
        username = "alex"
        response = self.client.get(DRIVER_LIST_URL + f"?username={username}")
        self.assertEqual(response.status_code, 200)

        expected_driver = get_user_model().objects.filter(
            username__icontains=username
        )
        self.assertIsNotNone(expected_driver)
        self.assertTrue(expected_driver.exists())
        self.assertEqual(
            list(response.context["driver_list"]),
            list(expected_driver)
        )

    def test_search_not_found(self):
        response = self.client.get(DRIVER_LIST_URL + "?username=invalid}")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["driver_list"]), 0)


DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverCreateViewTest(TestCase):
    def test_login_required(self):
        response = self.client.post(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverCreateViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="user",
            password="pass"
        )
        self.client.force_login(user)

    def test_valid_form_data(self):
        form_data = {
            "username": "user123",
            "first_name": "First test",
            "last_name": "Last test",
            "password1": "bad pass",
            "password2": "bad pass",
            "license_number": "NMK45908"
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        created_user: Driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(created_user.first_name, form_data["first_name"])
        self.assertEqual(created_user.last_name, form_data["last_name"])
        self.assertTrue(created_user.check_password(form_data["password1"]))
        self.assertEqual(
            created_user.license_number,
            form_data["license_number"]
        )

    def test_invalid_license_form_data(self):
        form_data = {
            "username": "user123",
            "first_name": "First test",
            "last_name": "Last test",
            "password1": "bad pass",
            "password2": "bad pass",
            "license_number": "N45908"
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        with self.assertRaises(Driver.DoesNotExist):
            get_user_model().objects.get(
                username=form_data["username"]
            )


DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=str(1))


class PublicDriverLicenseUpdateViewTest(TestCase):
    def test_login_required(self):
        response = self.client.post(DRIVER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverLicenseUpdateViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="user",
            password="pass"
        )
        self.client.force_login(user)

    def test_valid_form_data(self):
        _id = 1
        form_data = {
            "license_number": "NMK45908"
        }
        self.client.post(DRIVER_UPDATE_URL, data=form_data)
        updated_user: Driver = get_user_model().objects.get(pk=_id)

        self.assertEqual(
            updated_user.license_number,
            form_data["license_number"]
        )
