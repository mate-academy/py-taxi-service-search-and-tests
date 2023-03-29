from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverAdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="SupeAdmin",
            password="admin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="captain",
            first_name="Jack",
            last_name="Sparrow",
            password="BlackPerlTheBestShipEver",
            license_number="CJS99999",
        )

    def test_driver_license_in_list_display(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_in_fieldset(self):
        response = self.client.get(
            reverse("admin:taxi_driver_change", args=[self.driver.id])
        )
        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, "Additional info")

    def test_create_driver_add_fieldset(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))
        self.assertContains(response, "Additional info")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")


class CarAdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="SupeAdmin",
            password="admin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="captain",
            first_name="Jack",
            last_name="Sparrow",
            password="BlackPerlTheBestShipEver",
            license_number="CJS99999",
        )

    def test_driver_license_in_list_display(self):
        response = self.client.get(reverse("admin:taxi_car_changelist"))
        self.assertTrue(response.context)
