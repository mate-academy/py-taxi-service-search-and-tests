from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


class PrivateManufactureViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(
            name="namewith_i",
            country="wethout_char"
        )
        Manufacturer.objects.create(
            name="wethout_char",
            country="namewith_i"
        )
        Manufacturer.objects.create(
            name="wethout_char2",
            country="wethout_char_country"
        )
        Manufacturer.objects.create(
            name="namewith_i2",
            country="namewith_i3"
        )

    def test_manufacturer_list_search(self):

        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"manufacture_country": "i",
                                    "manufactur_name": "i"})
        self.assertEqual(
            list(response.context_data["manufacturer_list"]),
            list(Manufacturer.objects.filter(
                country__icontains="i"
            ).filter(name__icontains="i"))
        )

    def test_manufact_create_get_succses_redirect(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(path=url, data={
            "name": "Fuat12",
            "country": "dfwer"
        })
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_manufact_update_get_succses_redirect(self):
        url = reverse("taxi:manufacturer-update", args=["1"])
        response = self.client.post(path=url, data={
            "name": "Fuat123",
            "country": "dfwer1"
        })
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_manufact_delete_get_succses_redirect(self):
        url = reverse("taxi:manufacturer-delete", args=["1"])
        response = self.client.post(path=url)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
