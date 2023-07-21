from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class ManufacturerPublicTest(TestCase):

    def test_login_required_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEquals(res.status_code, 200)


class ManufacturedPrivateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testuser123"
        )
        self.client.force_login(self.user)

        self.instance = Manufacturer.objects.create(
            name="test1",
            country="TestCountry1"
        )

    def test_manufacturer_list(self):
        Manufacturer.objects.create(name="test3", country="TestCountry1")
        Manufacturer.objects.create(name="test2", country="TestCountry2")

        manufacturers = Manufacturer.objects.all()

        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_manufacturer_create(self):
        url = reverse("taxi:manufacturer-create")
        data = {"name": "test1", "country": "TestCountry1"}

        self.client.post(url, data)
        manufacturer = Manufacturer.objects.get()

        self.assertEqual(manufacturer.name, "test1")
        self.assertEquals(manufacturer.country, "TestCountry1")

    def test_manufacturer_update(self):
        url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.instance.id}
        )
        data = {"name": "changename", "country": "ChangeCountry"}

        response = self.client.post(url, data)

        self.instance.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.instance.name, "changename")
        self.assertEqual(self.instance.country, "ChangeCountry")

    def test_manufacturer_delete(self):
        url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.instance.id}
        )
        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.instance.id).exists()
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
