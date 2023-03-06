from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="1234qwer"
        )

    def test_driver_list_login_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_create_login_required(self):
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_license_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.driver.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="1234qwer"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_driver_create_login_required(self):
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(res.status_code, 200)

    def test_driver_license_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.driver.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_driver_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver.id}
        ))
        self.assertEqual(res.status_code, 200)
