from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_ID = 1
DRIVERS_LIST_URL = reverse("taxi:driver-list")
DRIVERS_DETAIL_URL = reverse("taxi:driver-detail", args=[DRIVERS_ID])


class PublicDriverTests(TestCase):
    def test_login_required(self):
        resp = self.client.get(DRIVERS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_page(self):
        get_user_model().objects.create_user(
            id=DRIVERS_ID,
            username="test",
            password="test1234",
            license_number="LIC12345",
        )

        resp = self.client.get(DRIVERS_DETAIL_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="LIC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_list_page(self):
        get_user_model().objects.create_user(
            username="First driver",
            password="first1234",
            license_number="FIR12345",
        )
        get_user_model().objects.create_user(
            username="Second driver",
            password="second1234",
            license_number="SEC12345",
        )

        resp = self.client.get(DRIVERS_LIST_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["driver_list"]),
            list(drivers),
        )

    def test_retrieve_detail_page(self):
        user_id = self.user.id

        resp = self.client.get(reverse("taxi:driver-detail", args=[user_id]))

        self.assertEqual(resp.status_code, 200)

    def test_search_form_list_page(self):
        get_user_model().objects.create_user(
            username="First driver",
            password="first1234",
            license_number="FIR12345",
        )
        get_user_model().objects.create_user(
            username="SECOND_DRIVER",
            password="second1234",
            license_number="SEC12345",
        )
        get_user_model().objects.create_user(
            username="Third",
            password="third1234",
            license_number="THI12345",
        )

        searching_data = {"username": "driver"}
        resp = self.client.get(DRIVERS_LIST_URL, data=searching_data)

        drivers = get_user_model().objects.filter(username__icontains="driver")

        self.assertEqual(
            list(resp.context["driver_list"]),
            list(drivers),
        )
