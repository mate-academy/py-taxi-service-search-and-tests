from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.tests.test_views.initial_data import (
    DRIVER_CREATE_URL,
    DRIVER_LIST_URL,
    DRIVER_DELETE_URL,
    DRIVERS_DATA
)
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm
)


class DriverChangesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.client.force_login(self.user)

    def test_successful_driver_creation(self):
        response = self.client.post(DRIVER_CREATE_URL, data=DRIVERS_DATA)
        driver = get_user_model().objects.get(username="test")
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            get_user_model().objects.filter(username="test").exists()
        )
        self.assertRedirects(
            response, reverse(
                "taxi:driver-detail",
                kwargs={"pk": driver.pk}
            )
        )

    def test_unsuccessful_driver_creation(self):
        data = {"username": "test"}
        response = self.client.post(DRIVER_CREATE_URL, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="test").exists()
        )

    def test_driver_creation_form_displayed_on_page(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertIsInstance(response.context["form"], DriverCreationForm)

    def test_driver_update_form_is_valid(self):
        form_data = {
            "license_number": "CBA54321"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_update_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.user.pk}
            ),
            data={"license_number": "CBA54321"}
        )
        self.assertRedirects(response, DRIVER_LIST_URL)

    def test_driver_successful_deletion_redirects_to_success_url(self):
        self.client.post(DRIVER_CREATE_URL, data=DRIVERS_DATA)
        driver = get_user_model().objects.get(username="test")
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.pk})
        )
        self.assertRedirects(response, DRIVER_LIST_URL)

    def test_successful_deletion_removes_driver_from_database(self):
        self.client.post(DRIVER_DELETE_URL)
        self.assertFalse(get_user_model().objects.filter(
            pk=self.user.pk
        ).exists())
