from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=["1"])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=["1"])


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_list_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_create_required(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_update_required(self):
        Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_delete_required(self):
        Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )

    def test_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_type_of_search_form(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(
            type(response.context["search_form"]),
            type(ManufacturerSearchForm())
        )


class PrivateManufacturerCreateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_success_url(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:manufacturer-list")
        )


class PrivateManufacturerUpdateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_success_url(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:manufacturer-list")
        )


class PrivateManufacturerDeleteTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_success_url(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:manufacturer-list")
        )
