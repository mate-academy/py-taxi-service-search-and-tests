from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverUsernameSearchForm


class TestDriverUsernameSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="johnson",
            password="johnson",
            license_number="JON26231",
        )
        get_user_model().objects.create_user(
            username="martin",
            password="martin",
            license_number="JON26232",
        )

    def test_driver_username_search_form(self):
        form_data = {"username": "admin"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form_username_search(self):
        form_data = {"username": "martin"}
        url = reverse("taxi:driver-list")
        response = self.client.get(url, data=form_data)
        self.assertContains(response, form_data["username"])
        self.assertNotContains(response, "johnson")
