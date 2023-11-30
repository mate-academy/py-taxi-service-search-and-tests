from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200, )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        number_of_manufacturers = 6
        for manufacturer_num in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"BMW {manufacturer_num}",
                country=f"Germany {manufacturer_num}"
            )

    def test_manufacturer_list_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view_url_accessible_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["manufacturer_list"]) == 5)

    def test_manufacturer_lists_all_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["manufacturer_list"]) == 1)


class PrivateManufacturerCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        self.form_data = {
            "name": "BMW",
            "country": "Germany",
        }

    def test_create_manufacturer(self):
        self.client.post(MANUFACTURER_CREATE_URL, data=self.form_data)
        new_manufacturer = Manufacturer.objects.get(
            name=self.form_data["name"]
        )
        self.assertEqual(new_manufacturer.name, self.form_data["name"])
        self.assertEqual(new_manufacturer.country, self.form_data["country"])

    def test_view_manufacturer_create_success_url(self):
        response = self.client.post(
            MANUFACTURER_CREATE_URL,
            data=self.form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/manufacturers/")
        self.assertRedirects(response, reverse_lazy("taxi:manufacturer-list"))


class PrivateManufacturerUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Spain"
        )

        self.data = {
            "name": "BMW",
            "country": "Germany",
        }

    def test_update_manufacturer(self):
        response = self.client.post(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}),
            self.data
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.country, "Germany")

    def test_view_manufacturer_update_success_url(self):
        response = self.client.post(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}),
            self.data
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertRedirects(response, "/manufacturers/")
        self.assertRedirects(response, reverse_lazy("taxi:manufacturer-list"))


class PrivateManufacturerDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Spain"
        )

    def test_manufacturer_delete_get_request(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id})
        )
        self.assertContains(response, "Delete manufacturer?")

    def test_manufacturer_delete_post_request(self):
        post_response = self.client.post(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id})
        )
        self.assertRedirects(
            post_response,
            reverse("taxi:manufacturer-list"),
            status_code=302
        )
