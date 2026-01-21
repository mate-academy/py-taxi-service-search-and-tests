from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.tests.test_views.initial_data import DRIVERS_DATA


class DriverChangesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.client.force_login(self.user)

    def test_successful_driver_creation(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=DRIVERS_DATA
        )
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
        response = self.client.post(reverse("taxi:driver-create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="test").exists()
        )

    def test_driver_creation_form_displayed_on_page(self):
        response = self.client.get(reverse("taxi:driver-create"))
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
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_driver_successful_deletion_redirects_to_success_url(self):
        self.client.post(reverse("taxi:driver-create"), data=DRIVERS_DATA)
        driver = get_user_model().objects.get(username="test")
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.pk})
        )
        self.assertRedirects(
            response,
            reverse("taxi:driver-list")
        )

    def test_successful_deletion_removes_driver_from_database(self):
        self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.user.pk})
        )
        self.assertFalse(get_user_model().objects.filter(
            pk=self.user.pk
        ).exists())
