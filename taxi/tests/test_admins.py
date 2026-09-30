from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.admin import CarAdmin


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="Vasia",
            password="123123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="Tolkia",
            password="123123",
            license_number="HFN11111",
        )

    def test_admin(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.license_number)

    def test_car(self):
        self.assertEqual(CarAdmin.list_filter, ("manufacturer", ))
