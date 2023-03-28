from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Nissan", country="Japan")
        response = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL + "?name=Toyota")
        expected_queryset = Manufacturer.objects.filter(
            name__icontains="Toyota"
        )

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            expected_queryset
        )

    def test_driver_creation(self):
        form_data = {
            "username": "driver_user",
            "password1": "drive12345",
            "password2": "drive12345",
            "first_name": "Driver First",
            "last_name": "Driver Last",
            "license_number": "TES12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
