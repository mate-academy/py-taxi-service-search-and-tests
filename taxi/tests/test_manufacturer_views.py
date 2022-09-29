from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.views import ManufacturerListView

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTests(TestCase):

    def test_login_required_manufacturer_list_url(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_create_url(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_delete_url(self):
        self.manufacturer = Manufacturer.objects.create(name="test_man1", country="UK")
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_login_required_manufacturer_update_url(self):
        self.manufacturer3 = Manufacturer.objects.create(name="test_man3", country="UK")
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer3.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password1",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)
        number_of_manufacturers = 5
        for index in range(number_of_manufacturers):
            self.index = Manufacturer.objects.create(
                name="Test" + str(index),
                country="India"
            )

    def test_get_data_from_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_queryset(self):
        """test that view return right filtered queryset"""

        response = RequestFactory().get("manufacturers/?name=3")
        view = ManufacturerListView()
        view.request = response
        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Manufacturer.objects.filter(name__icontains="3"))

    def test_create_manufacturer(self):
        form_data = {
            "name": "test1_man",
            "country": "UK_test"
        }

        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        print(new_manufacturer)

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])
