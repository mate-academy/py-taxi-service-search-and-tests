from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


class ViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password1234"
        )

        self.client.force_login(self.user)

    def test_manufacturer_list(self):
        manufacturer_list_url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Zaporoshetz",
            country="Ukraine"
        )

        response = self.client.get(manufacturer_list_url)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        manufacturer_list_url = reverse("taxi:manufacturer-list")

        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Zaporoshetz",
            country="Ukraine"
        )

        response = self.client.get(manufacturer_list_url + "?name=b")

        manufacturers = Manufacturer.objects.all()

        self.assertNotEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
