from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm

DRIVER_ID = 1
DRIVERS_LIST_URL = reverse("taxi:driver-list")
DRIVERS_DETAIL_URL = reverse("taxi:driver-detail", args=[DRIVER_ID])


class PublicDriverTests(TestCase):
    def test_login_required(self):
        resp = self.client.get(DRIVERS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_page(self):
        get_user_model().objects.create_user(
            id=DRIVER_ID,
            username="test_username",
            password="testpassword12345",
            license_number="ADR12348",
        )

        resp = self.client.get(DRIVERS_DETAIL_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            id=DRIVER_ID,
            username="test_username",
            password="testpassword12345",
            license_number="ADR12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_list_page_with_search_field(self):
        get_user_model().objects.create_user(
            username="driver1",
            password="first1234",
            license_number="BBB12345",
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="second1234",
            license_number="TAR12345",
        )

        resp = self.client.get(DRIVERS_LIST_URL)

        drivers = get_user_model().objects.all()
        form = DriverSearchForm()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["driver_list"]),
            list(drivers),
        )
        self.assertEqual(
            resp.context["driver_search_form"].is_valid(),
            form.is_valid()
        )

    def test_retrieve_detail_page(self):
        user_id = self.user.id

        resp = self.client.get(reverse("taxi:driver-detail", args=[user_id]))
        driver = get_user_model().objects.get(id=user_id)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context["driver"],
            driver
        )
