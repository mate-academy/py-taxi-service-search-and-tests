from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test", password="Testpass123"
        )

    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test", password="Testpass123"
        )
        self.client.force_login(self.driver)


class PrivateDriverListTests(BasePrivateDriverTests):
    DRIVER_LIST_URL = reverse("taxi:driver-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(1, 11):
            get_user_model().objects.create_user(
                username=f"Test driver {i}",
                password="Testpass123",
                license_number=f"TST1234{i}",
            )

    def test_driver_list_template(self):
        response = self.client.get(self.DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_pagination(self):
        response = self.client.get(self.DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["driver_list"]),
            self.VIEW_PAGINATED_BY
        )

    def test_driver_list_search(self):
        response = self.client.get(self.DRIVER_LIST_URL + "?username=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 2)
        self.assertContains(response, "Test driver 1")
        self.assertNotContains(response, "Test driver 2")

    def test_driver_search_pagination(self):
        response = self.client.get(
            self.DRIVER_LIST_URL + "?username=Test&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["driver_list"]),
            self.VIEW_PAGINATED_BY
        )


class PrivateDriverDetailTests(BasePrivateDriverTests):
    def test_driver_detail_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PrivateDriverCreateTests(BasePrivateDriverTests):
    def test_driver_create_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_create_post(self):
        form_data = {
            "username": "new_test_driver",
            "license_number": "TST12345",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_driver.username, form_data["username"])
        self.assertTrue(new_driver.check_password(form_data["password1"]))


class PrivateDriverLicenseUpdateTests(BasePrivateDriverTests):
    def test_driver_license_update_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_license_update_post(self):
        form_data = {
            "license_number": "UPD54321",
        }
        self.client.post(
            reverse("taxi:driver-update", args=[self.driver.id]),
            data=form_data
        )
        updated_driver = get_user_model().objects.get(id=self.driver.id)
        self.assertEqual(
            updated_driver.license_number,
            form_data["license_number"]
        )


class PrivateDriverDeleteTests(BasePrivateDriverTests):
    def test_driver_delete_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_driver_delete_post(self):
        self.client.post(reverse("taxi:driver-delete", args=[self.driver.id]))
        drivers = get_user_model().objects.filter(id=self.driver.id)
        self.assertEqual(len(drivers), 0)
