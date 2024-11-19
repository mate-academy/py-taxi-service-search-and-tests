from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class PublicManufacturerViewsTest(TestCase):
    def test_manufacturer_list_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

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


class PrivateManufacturerViewsTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Another Manufacturer", country="Test Country2"
        )
        self.driver = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Username",
            license_number="AAA12345",
            password="1qaz3edc",
        )
        self.client.force_login(self.driver)

    def test_search_form_with_valid_data(self):
        form = ManufacturerSearchForm(data={"name": self.manufacturer1.name})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], self.manufacturer1.name)

    def test_search_form_with_empty_data(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), data={"name": "Test"}
        )
        self.assertContains(response, "Test Manufacturer")
        self.assertNotContains(response, "Another Manufacturer")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), data={"name": "Another"}
        )
        self.assertContains(response, "Another Manufacturer")
        self.assertNotContains(response, "Test Manufacturer")
