from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
        )
        self.client.force_login(self.admin_user)

    def test_driver_list_display_has_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(
            response,
            get_user_model().objects.get(pk=1).license_number
        )

    def test_driver_change_has_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[1])
        response = self.client.get(url)
        self.assertContains(
            response,
            get_user_model().objects.get(pk=1).license_number
        )

    def test_driver_add_has_additional_info(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "Additional info")
        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "License number:")

    def test_car_has_filter(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "By manufacturer")

    def test_car_has_search_field(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(
            response,
            '<input type="submit" value="Search">'
        )
