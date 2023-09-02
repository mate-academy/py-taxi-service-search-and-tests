from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListTests(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Manufacturer.objects.create(name="ABCD", country="Country")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers_by_name(self):
        search_param = "abba"
        search_manufacturer_url = MANUFACTURER_URL + "?name=" + search_param

        response = self.client.get(search_manufacturer_url)
        manufacturers = Manufacturer.objects.filter(
            name__icontains=search_param
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PublicManufacturerCreateTests(TestCase):
    def test_public_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerCreateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")


class PublicManufacturerUpdateTests(TestCase):
    def test_public_login_required(self):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="ABBA", country="Sweden")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_update_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        )
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["manufacturer"], manufacturer)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")


class PublicManufacturerDeleteTests(TestCase):
    def test_public_login_required(self):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="ABBA", country="Sweden")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_delete_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["manufacturer"], manufacturer)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_confirm_delete.html"
        )
