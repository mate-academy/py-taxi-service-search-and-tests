from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class TestAdmin(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test1234",
            license_number="1234",
            first_name="John",
            last_name="Doe",
            email="example@email.com"
        )
        self.client.force_login(self.admin)

    def test_list_display(self):
        response = self.client.get("/admin/taxi/driver/")
        self.assertContains(response, self.admin.license_number)

    def test_fieldsets(self):
        response = self.client.get(f"/admin/taxi/driver/{self.admin.pk}/change/")
        self.assertContains(response, self.admin.license_number)

    def test_add_fieldsets(self):
        response = self.client.get(f"/admin/taxi/driver/add/")
        self.assertContains(response, "Additional info")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")
