from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


URL_MANUFACTURER_LIST = "taxi:manufacturer-list"


class PublicManufacturerViewTest(TestCase):
    def test_manufacturer_login_required(self) -> None:
        response = self.client.get(reverse(URL_MANUFACTURER_LIST))

        self.assertRedirects(
            response,
            "/accounts/login/?next=/manufacturers/"
        )


class PrivateManufacturerViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            license_number="AAA55555"
        )

        self.client.force_login(self.user)

    def test_manufacturer_correct_template(self) -> None:
        response = self.client.get(reverse(URL_MANUFACTURER_LIST))

        self.assertEqual(str(response.context["user"]), "test_username ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_list(self) -> None:
        Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine",
        )

        response = self.client.get(reverse(URL_MANUFACTURER_LIST))
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_list_search(self) -> None:
        Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine",
        )

        response = self.client.get(reverse(URL_MANUFACTURER_LIST) + "?name=Tavria")
        tavria = Manufacturer.objects.filter(name="Tavria")

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(tavria)
        )
