from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            first_name="First",
            last_name="Last",
            license_number="HHH12345"
        )

    def test_driver_license_number_listed(self):
        """Tests that driver's license number is in list_display
         an driver admin page"""

        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """Tests that driver's license number is in an driver detail
         admin page"""

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fields_listed(self):
        """Tests that driver's first name, last name,
         license number are an driver add admin page"""

        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
