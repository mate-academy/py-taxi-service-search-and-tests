from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Driver

DRIVER_LIST = reverse("taxi:driver-list")


class PublicDriverViewListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="jim.hopper",
            license_number="AAA12345"
        )
        Driver.objects.create(
            username="driver3",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="driver1",
            license_number="CCC12345"
        )

    def test_create_driver(self):
        form_data = {
            "username": "driver3",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_list_view_search(self):
        """
        Search for driver with the username 'Toyota'
        Verify that the search form is present in the context
        Verify that the filtered manufacturers are present in the context
        """
        form_data = {
            "username": "jim.hopper",
        }
        response = self.client.get(reverse("taxi:driver-list"), data=form_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["search_form"]
        self.assertIsInstance(form, DriverSearchForm)

        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 1)
        self.assertEqual(driver_list[0].username, "jim.hopper")
