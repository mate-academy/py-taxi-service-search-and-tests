from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_when_user_logout(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next=/manufacturers/"
        )


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_name", country="test_country")

        Manufacturer.objects.create(name="test_Tesla", country="test_USA")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_on_manufacturers_list_page(self):
        Manufacturer.objects.create(
            name="test_2131231231", country="test_country_13131"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "test_2131231231"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(
                name__icontains="test_2131231231")
            ),
        )
