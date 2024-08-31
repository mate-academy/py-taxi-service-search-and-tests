from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )

    def test_login_required_for_driver_list(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_driver_detail(self):
        res = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.user.id])
        )
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_driver_update(self):
        res = self.client.get(reverse(
            "taxi:driver-update",
            args=[self.user.id])
        )
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_driver_delete(self):
        res = self.client.get(reverse(
            "taxi:driver-delete",
            args=[self.user.id])
        )
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="Test1",
            password="test1231",
            license_number="ABC12344"
        )
        get_user_model().objects.create_user(
            username="Test2",
            password="test1232",
            license_number="ABC12345"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        driver_list = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
