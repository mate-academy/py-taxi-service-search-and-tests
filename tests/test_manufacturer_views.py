from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse

from taxi.models import Driver, Car, Manufacturer


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)

    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_update_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id]))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)
        self.manufacturer2 = Manufacturer.objects.create(name="BMW",
                                                         country="Germany")
        self.manufacturer3 = Manufacturer.objects.create(name="	BAIC",
                                                         country="	China")
        self.manufacturers = Manufacturer.objects.all()

    def test_retrieve_manufacturers_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(self.manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "BAIC")

    def test_manufacturer_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=nonexistent")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context["manufacturer_list"]),
                            list(self.manufacturers))
