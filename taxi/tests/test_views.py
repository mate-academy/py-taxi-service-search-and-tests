from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_VIEW_URL = reverse("taxi:manufacturer-list")


class ManufacturerGetAccessCheck(TestCase):
    def test_manufacturer_list_view_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)


class ManufacturerTestWithLoggedInUser(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="123admin123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="ZAZ", country="Ukraine")

    def test_retrieve_manufacturer_list_view(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "test",
            "country": "test",
        }

        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_manufacturer_search(self):
        response = self.client.get("/manufacturers/?name=Fo")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["manufacturer_list"],
                                 Manufacturer.objects.filter(name__icontains="Fo"))
