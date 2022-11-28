from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        """test client login on list_manufacturer"""
        response = self.client.get(MANUFACTURER_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_create_manufacturer_list_required(self):
        """test client create the user profile on list_manufacturer"""
        response = self.client.get("taxi:manufacturer-create")
        self.assertNotEqual(response.status_code, 200)


class PrivetManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwer1234"
        )
        self.client.force_login(self.user)

    def test_create_required_manufacturer_list_with_login(self):
        """test should create the name and country and expect it"""
        Manufacturer.objects.create(name="test", country="Countrytest")
        response = self.client.get(MANUFACTURER_LIST)

        self.assertEqual(response.status_code, 200)

    def test_required_queryset_in_db_manufacturer_with_login(self):
        """test should required the name and country in db"""
        Manufacturer.objects.create(name="test", country="Countrytest")
        manufacturer_all = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST)

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer_all)
        )

    def test_link_template_should_be_manufacturer_list_with_login(self):
        """test should required template in right link"""
        Manufacturer.objects.create(name="test", country="Countrytest")
        response = self.client.get(MANUFACTURER_LIST)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_update_required_in_detail_manufacturer_with_login(self):
        """test should update the manufacturer"""
        manufacturer_update = Manufacturer.objects.create(
            name="test", country="Countrytest")
        url_to_update = reverse(
            "taxi:manufacturer-update", args=[manufacturer_update.id]
        )
        response = self.client.get(url_to_update)
        self.assertEqual(response.status_code, 200)

    def test_delete_required_in_detail_manufacturer_with_login(self):
        """test should delete the manufacturer"""
        manufacturer_delete = Manufacturer.objects.create(
            name="test", country="Countrytest")
        url_to_delete = reverse(
            "taxi:manufacturer-delete", args=[manufacturer_delete.id]
        )
        response = self.client.post(url_to_delete)
        self.assertEqual(response.status_code, 302)


class SearchDriverTests(TestCase):
    """test the search manufacturer field"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_field(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="test")),
        )
