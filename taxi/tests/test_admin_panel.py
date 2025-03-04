from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverAdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            license_number="AAA11111",
        )

        self.client.force_login(self.admin_user)

    def test_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.admin_user.license_number)

    def test_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.admin_user.id])
        response = self.client.get(url)
        self.assertContains(response, "AAA11111")

    def test_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.post(
            url,
            {
                "username": "User",
                "password1": "1qazcde3",
                "password2": "1qazcde3",
                "license_number": "BBB22222",
                "first_name": "user first",
                "last_name": "user last"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter(first_name="user first").exists()
        )
