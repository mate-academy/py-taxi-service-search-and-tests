from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        """test client login on driver_list"""
        response = self.client.get(DRIVER_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_create_manufacturer_list_required(self):
        """test client create the user profile on driver_list"""
        response = self.client.get("taxi:driver-create")
        self.assertNotEqual(response.status_code, 200)


class PrivetManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwer1234"
        )
        self.client.force_login(self.user)

    def test_create_required_driver_list_with_login(self):
        """test should create the driver list and expect it"""
        Driver.objects.create(
            first_name="test first",
            last_name="test last",
            license_number="TES12345"
        )
        response = self.client.get(DRIVER_LIST)

        self.assertEqual(response.status_code, 200)

    def test_required_queryset_in_db_manufacturer_with_login(self):
        """test should required the driver list in db"""
        Driver.objects.create(
            first_name="test first",
            last_name="test last",
            license_number="TES12345")
        driver_all = Driver.objects.all()
        response = self.client.get(DRIVER_LIST)

        self.assertEqual(
            list(response.context["driver_list"]), list(driver_all)
        )

    def test_link_template_should_be_manufacturer_list_with_login(self):
        """test should required template in right link"""
        Driver.objects.create(
            first_name="test first",
            last_name="test last",
            license_number="TES12345"
        )
        response = self.client.get(DRIVER_LIST)

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_update_required_in_detail_manufacturer_with_login(self):
        """test should update the driver detail list"""
        driver_update = Driver.objects.create(
            first_name="test first",
            last_name="test last",
            license_number="TES12345"
        )
        url_to_update = reverse(
            "taxi:driver-update", args=[driver_update.id]
        )
        response = self.client.get(url_to_update)
        self.assertEqual(response.status_code, 200)


class SearchDriverTests(TestCase):
    """test the search driver field"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_driver_search_field(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="test")),
        )
