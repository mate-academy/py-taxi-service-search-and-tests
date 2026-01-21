from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from taxi.models import Manufacturer

MANUFACTURER_LIST_VIEW_URL = reverse_lazy("taxi:manufacturer-list")
MANUFACTURER_CREATE_VIEW_URL = reverse_lazy("taxi:manufacturer-create")


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self):
        driver_user = get_user_model().objects.create_user(
            username="driver_1",
            password="user_password",
        )
        self.client.force_login(driver_user)

        manufacturers_rare = [
            Manufacturer(name="BWM"),
            Manufacturer(name="Audi"),
            Manufacturer(name="Porsche"),
        ]

        Manufacturer.objects.bulk_create(manufacturers_rare)

        self.manufacturers = Manufacturer.objects.all()
        self.response = self.client.get(MANUFACTURER_LIST_VIEW_URL)

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)

        self.assertEqual(response.status_code, 200)

    def test_list_view_should_contain_data(self):
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(self.manufacturers),
        )

    def test_search_form_list_view(self):
        data = {
            "name": "BWM"
        }

        self.manufacturers = Manufacturer.objects.filter(
            name__icontains=data["name"]
        )

        self.response = self.client.get(MANUFACTURER_LIST_VIEW_URL, data=data)

        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(self.manufacturers),
        )


class PrivateManufacturerCreateViewTest(TestCase):
    def setUp(self):
        driver_user = get_user_model().objects.create_user(
            username="driver_1",
            password="user_password",
        )

        self.form_data = {
            "name": "M-1",
            "country": "C-1",
        }

        self.client.force_login(driver_user)
        self.response = self.client.get(MANUFACTURER_CREATE_VIEW_URL)

    def test_login_required(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_create_view(self):
        self.response = self.client.post(
            MANUFACTURER_CREATE_VIEW_URL, data=self.form_data
        )

        created_manufacturer = Manufacturer.objects.get(name="M-1")

        self.assertEqual(created_manufacturer.name, self.form_data["name"])
        self.assertEqual(
            created_manufacturer.country,
            self.form_data["country"]
        )
