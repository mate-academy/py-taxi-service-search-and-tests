from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class TestDriverAdmin(TestCase):
    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )

        self.client = Client()
        self.client.force_login(self.superuser)

        self.url = "http://127.0.0.1:8000/admin/taxi/driver/"

    def test_driver_list_license_number(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.superuser.license_number)
