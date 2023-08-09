from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[1])
DRIVER_LICENSE_UPDATE_URL = reverse("taxi:driver-update", args=[1])


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        response = self.client.get(DRIVER_DELETE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_license_update_login_required(self):
        response = self.client.get(DRIVER_LICENSE_UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        drivers = get_user_model().objects.all()
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        driver = get_user_model().objects.get(id=1)
        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
