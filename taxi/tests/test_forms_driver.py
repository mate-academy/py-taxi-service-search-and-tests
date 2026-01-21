from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_URL = reverse("taxi:driver-list")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="qwe",
            password="test123",
            license_number="AA1",
        )
        get_user_model().objects.create_user(
            username="zxc",
            password="test123",
            license_number="AA2",
        )

    def test_driver_search_without_query(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "qwe")
        self.assertContains(res, "zxc")

    def test_driver_search_with_correct_query(self):
        res = self.client.get(DRIVER_URL, {"username": "qw"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "qwe")
        self.assertNotContains(res, "zxc")

    def test_driver_search_with_wrong_query(self):
        res = self.client.get(DRIVER_URL, {"username": "YYY"})
        self.assertNotContains(res, "qwe")
        self.assertNotContains(res, "zxc")
