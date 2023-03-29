from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = "taxi:driver-detail"
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = "taxi:driver-update"
DRIVER_DELETE_URL = "taxi:driver-delete"
PAGINATION = 5

TestCase.fixtures = ["taxi_service_db_data.json", ]


class PublicDriverViewsTests(TestCase):

    def test_login_required_for_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_detail_view(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_create_view(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_update_view(self):
        driver = Driver.objects.get(id=1)
        response = self.client.get(
            reverse(DRIVER_UPDATE_URL, kwargs={"pk": driver.id})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_delete_view(self):
        driver = Driver.objects.get(id=1)
        response = self.client.post(
            reverse(DRIVER_DELETE_URL, kwargs={"pk": driver.id})
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_driver_list_view_response_with_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_view_is_paginated(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), PAGINATION)

    def test_driver_list_view_search_by_username(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTrue(
            "username" in response.context_data["search_form"].fields
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        driver_list = list(Driver.objects.all()[:PAGINATION])
        self.assertEqual(list(response.context["driver_list"]), driver_list)


class PrivateDriverDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_driver_detail_view_response_with_correct_template(self):
        response = self.client.get(
            reverse(DRIVER_DETAIL_URL, kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PrivateDriverCreateVewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_driver_create_view_response_with_correct_template(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_driver(self):
        form_data = {
            "username": "Test_username",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "test_password_123",
            "password2": "test_password_123",
            "license_number": "TES11111"
        }
        response = self.client.post(reverse("taxi:driver-create"), form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )


class PrivateDriverLicenseUpdateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_driver_license_update_view_response_with_correct_template(self):
        response = self.client.get(
            reverse(DRIVER_UPDATE_URL, kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_license_update_view_has_correct_success_url(self):
        response = self.client.get(
            reverse(DRIVER_UPDATE_URL, kwargs={"pk": self.user.id})
        )
        self.assertEqual(
            response.context_data["view"].success_url, DRIVER_LIST_URL
        )

    def test_update_driver_license_with_valid_data(self):
        response = self.client.post(
            reverse(DRIVER_UPDATE_URL, kwargs={"pk": self.user.id}),
            {"license_number": "UPD00000"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            get_user_model().objects.get(id=self.user.id).license_number,
            "UPD00000"
        )

    def test_update_driver_license_with_not_valid_data(self):
        response = self.client.post(
            reverse(DRIVER_UPDATE_URL, kwargs={"pk": self.user.id}),
            {"license_number": "test1"}
        )
        self.assertEqual(response.status_code, 200)


class PrivateDriverDeleteViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_driver_delete_view_response_with_correct_template(self):
        response = self.client.get(
            reverse(DRIVER_DELETE_URL, kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_driver_delete_view_has_correct_success_url(self):
        response = self.client.get(
            reverse(DRIVER_DELETE_URL, kwargs={"pk": self.user.id})
        )
        self.assertEqual(
            response.context_data["view"].success_url, DRIVER_LIST_URL
        )

    def test_delete_driver(self):
        driver = get_user_model().objects.create(
            username="driver",
            first_name="first_name",
            last_name="last_name",
            license_number="LIC00000",
        )
        response = self.client.post(
            reverse(DRIVER_DELETE_URL, kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(username="driver").exists()
        )
