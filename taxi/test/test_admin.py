from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author", password="testauthor", license_number="Test"
        )

    def test_driver_listed(self):
        """
        test that authors pseudonym is in list_display on admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_author_in_detail(self):
        """
        Test that author's pseudonym is on author detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_form_has_license_number_field(self):
        """
        Test that the author add form includes the pseudonym field
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, 'name="license_number"')
