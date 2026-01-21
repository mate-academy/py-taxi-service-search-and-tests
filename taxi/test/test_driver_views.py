from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})


class DriverListTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_correct_pagination(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_correct_search_form_present(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTrue("search_form" in response.context)
        self.assertTrue(
            isinstance(response.context["search_form"],
                       DriverSearchForm)
        )

    def test_search_form_correct_output(self):
        url = DRIVER_LIST_URL + "?" + urlencode({"username": "wheeler"})
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(
                username__icontains="wheeler"
            )),
        )


class DriverDetailTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class DriverCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_correct_redirect_after_driver_create(self):
        response = self.client.post(
            DRIVER_CREATE_URL,
            {
                "username": "new_user",
                "password1": "test_password",
                "password2": "test_password",
                "license_number": "ABC12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("taxi:driver-detail", kwargs={"pk": 2})
        )


class DriverUpdateTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_correct_redirect_after_driver_update(self):
        response = self.client.post(
            DRIVER_UPDATE_URL,
            {
                "license_number": "ABC12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, DRIVER_LIST_URL)


class DriverDeleteTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_driver_deleted(self):
        response = self.client.post(DRIVER_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(pk=1).exists())

    def test_correct_redirect_after_driver_delete(self):
        response = self.client.post(DRIVER_DELETE_URL)
        self.assertRedirects(response, reverse("taxi:driver-list"))


class LoginRequiredTests(TestCase):
    def test_driver_list_restricted_to_logged_in(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_restricted_to_logged_in(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_restricted_to_logged_in(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_restricted_to_logged_in(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_restricted_to_logged_in(self):
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)
