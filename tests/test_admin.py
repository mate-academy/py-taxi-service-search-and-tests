from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminPanelTest(TestCase):
    USERNAME = "testuser"
    PASSWORD = "qwe12G$z_R"
    FIRST_NAME = "Testjohn"
    LAST_NAME = "Testjohnson"
    LICENSE_NUMBER = "ADD456431"

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="testadmin",
            password="testpassword123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            license_number=self.LICENSE_NUMBER,
        )

    def test_license_number_is_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_is_license_listed_in_detail_view(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        resource = self.client.get(url)
        self.assertContains(resource, self.driver.license_number)

    def test_required_fields_existing_in_detail_view(self):
        fields = ["first_name", "last_name", "license_number"]
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        for field in fields:
            self.assertContains(response, field)
