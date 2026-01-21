from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="testTest",
            password="testTest123"
        )
        self.client.force_login(self.admin_user)

    def test_admin_car_change_list(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_admin_driver_change_list(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
