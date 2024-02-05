from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPanelTest(TestCase):
    """
    TestCase class for testing the admin panel functionality.
    """

    def setUp(self) -> None:
        """
        Set up necessary data for the tests.
        """
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_FSDLJK_6354",
            password="Some9Complex0Password7"
        )

        self.driver = get_user_model().objects.create_user(
            username="driver_KLFPW_345",
            password="Dri#$^ver_22#$34_pas^#%s_54@#22",
            first_name="Mykola",
            last_name="Meatball",
            license_number="FTL12345"
        )

        self.client.force_login(self.admin_user)

    def test_drivers_list_display_license_number(self):
        """
        Test if the drivers list in the admin panel displays the license number
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_fieldsets_additional_info_license_number(self):
        """
        Test if the additional info fieldsets for a driver also display the
        license number.
        """
        url = reverse(
            "admin:taxi_driver_change",
            kwargs={"object_id": self.driver.id}
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_add_fieldsets_additional_info_first_name_last_name_ln(self):
        """
        Test if the add_fieldsets for a driver display the required fields
        correctly.
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
