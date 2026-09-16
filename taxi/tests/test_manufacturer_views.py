from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-list")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_get_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(Manufacturer.objects.all()),
            list(response.context["object_list"]),
        )

    def test_search_manufacturer_list(self):
        ford = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        response = self.client.get(self.url, {"name": "ford"})
        self.assertIn(ford, response.context["object_list"])
        self.assertNotIn(toyota, response.context["object_list"])

    def test_search_empty_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        response = self.client.get(self.url, {"name": "toyota"})
        self.assertEqual(0, len(response.context["object_list"]))


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-create")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_create_manufacturer_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_can_create_manufacturer(self):
        response = self.client.post(
            self.url,
            data={
                "name": "Ford",
                "country": "USA",
            }
        )
        manufacturer = Manufacturer.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(Manufacturer.objects.count(), 1)
        self.assertEqual(manufacturer.country, "USA")
        self.assertEqual(manufacturer.name, "Ford")

    def test_create_errors(self):
        response = self.client.post(
            self.url,
            data={"name": "Ford", "country": ""}
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, "country", "This field is required.")


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="ford",
            country="usa",
        )
        self.url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.pk},
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_update_manufacturer_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")
        self.assertEqual(self.manufacturer, response.context["object"])

    def test_can_update_manufacturer(self):
        response = self.client.post(
            self.url,
            data={"name": "Ford", "country": "USA"}
        )
        self.manufacturer.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual("USA", self.manufacturer.country)
        self.assertEqual("Ford", self.manufacturer.name)

    def test_update_errors(self):
        response = self.client.post(
            self.url,
            data={"name": "", "country": ""}
        )
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, "name", "This field is required.")
        self.assertFormError(form, "country", "This field is required.")


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        self.url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.pk},
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_manufacturer_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"),
        self.assertEqual(self.manufacturer, response.context["object"])

    def test_can_delete_manufacturer(self):
        response = self.client.post(
            self.url,
        )
        pk = self.manufacturer.pk
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(Manufacturer.objects.filter(id=pk).exists())
