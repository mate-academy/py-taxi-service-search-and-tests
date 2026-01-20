from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


class SearchMixinTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )
        self.client.force_login(self.driver)
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                         country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford",
                                                         country="USA")
        self.manufacturer3 = Manufacturer.objects.create(name="Honda",
                                                         country="Japan")

    def test_search_form_filtering(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota")
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")
        self.assertEqual(response.context["search_form"].initial["name"],
                         "Toyota")

    def test_search_form_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW")
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 0)

    def test_search_form_empty_query(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 3)

    def test_search_form_invalid(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=123")
        manufacturers = response.context["manufacturer_list"]
        self.assertNotEqual(len(manufacturers), 3)
