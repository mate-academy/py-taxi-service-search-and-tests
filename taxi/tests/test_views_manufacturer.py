from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class PublicManufacturerlistTest(TestCase):
    def test_manufacturer_list(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_update_login_required(self):
        url = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": manufacturer.id}
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateAlllistTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Another Manufacturer", country="Test Country2"
        )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.driver)

    def test_manufacturer_list(self):
        Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        Manufacturer.objects.create(
            name="test_china",
            country="China",
        )
        respons = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(respons.status_code, 200)

    def test_manufacturer_search_list(self):
        Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        Manufacturer.objects.create(
            name="test_china",
            country="China",
        )
        form = ManufacturerSearchForm(data={"name": self.manufacturer1.name})
        respons = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(respons.status_code, 200)
        self.assertEqual(
            list(respons.context["manufacturer_list"]),
            list(Manufacturer.objects.all()))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], self.manufacturer1.name)
        self.assertTemplateUsed(respons, "taxi/manufacturer_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), data={"name": "Test"}
        )
        print(response)
        self.assertContains(response, "Test Manufacturer")
        self.assertNotContains(response, "Another Manufacturer")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), data={"name": "Another"}
        )
        self.assertContains(response, "Another Manufacturer")
        self.assertNotContains(response, "Test Manufacturer")
