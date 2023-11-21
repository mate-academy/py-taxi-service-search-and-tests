from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_ID = 1
DRIVERS_LIST_URL = reverse("taxi:driver-list")
DRIVERS_DETAIL_URL = reverse("taxi:driver-detail", args=[DRIVERS_ID])


class PublicDriverViewTests(TestCase):
    def test_login_required(self):
        resp = self.client.get(DRIVERS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_page(self):
        get_user_model().objects.create_user(
            id=DRIVERS_ID,
            username="TEST",
            password="Test1234!",
            license_number="ABC12345",
        )

        resp = self.client.get(DRIVERS_DETAIL_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateDriverViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Driver1",
            password="Test1234!",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_get_driver_list_page(self):
        get_user_model().objects.create_user(
            username="Driver2",
            password="Test1234!",
            license_number="BCD12345",
        )
        get_user_model().objects.create_user(
            username="Driver3",
            password="Test1234!",
            license_number="CDE12345",
        )

        resp = self.client.get(DRIVERS_LIST_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["driver_list"]),
            list(drivers),
        )

    def test_get_driver_detail_page(self):

        resp = self.client.get(reverse("taxi:driver-detail", args=[self.user.id]))
        license_number = resp.context["user"].license_number

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(license_number, self.user.license_number)
