from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required_list_page(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="test_name1")
        Manufacturer.objects.create(name="test_name2")

    def test_retrive_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_manufacturer_search_queryset(self):
        manufacturer_in_res_queryset = Manufacturer.objects.create(
            name="Test-in queryset"
        )
        manufacturer_not_in_res_queryset = Manufacturer.objects.create(
            name="Test-not-in queryset"
        )
        url = MANUFACTURER_URL + "?name=Test-in"
        response = self.client.get(url)
        self.assertContains(response, manufacturer_in_res_queryset.name)
        self.assertNotContains(response, manufacturer_not_in_res_queryset.name)
