from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTest(TestCase):

    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        number_of_manufacturers = 13

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name="Test Manufacturer" + str(manufacturer_id),
                country="Test Country",
            )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_five(self):
        self.client.force_login(self.user)
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        self.client.force_login(self.user)
        response = self.client.get(self.MANUFACTURER_URL + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 3)


class ManufacturerCreateViewTest(TestCase):
    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_success_url(self):
        self.client.force_login(self.user)

        form_data = {
            "name": "Another Manufacturer", "country": "Another Country"
        }

        response = self.client.post(reverse(
            "taxi:manufacturer-create"), data=form_data
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(Manufacturer.objects.count(), 2)

    def test_form_displayed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")
        self.assertContains(response, "name")

    def test_create_with_invalid_data(self):
        self.client.force_login(self.user)

        form_data = {"name": "", "country": "Country"}
        response = self.client.post(reverse(
            "taxi:manufacturer-create"), data=form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "name", "This field is required."
        )
        self.assertEqual(Manufacturer.objects.count(), 1)


class ManufacturerUpdateViewTest(TestCase):
    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template_after_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data={"name": "New Name", "country": "New Country"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertContains(response, "New Name")

    def test_update_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        form_data = {"name": "", "country": "New Country"}
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "name", "This field is required."
        )

        self.manufacturer.refresh_from_db()
        self.assertNotEqual(self.manufacturer.name, "")


class ManufacturerDeleteViewTest(TestCase):
    MANUFACTURER_DELETE_URL_NAME = "taxi:manufacturer-delete"

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_view(self):
        self.client.force_login(self.user)
        url = reverse(
            self.MANUFACTURER_DELETE_URL_NAME,
            args=[self.manufacturer.id]
        )
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(Manufacturer.objects.count(), 0)


class ManufacturerSearchFormTest(TestCase):
    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        number_of_manufacturers = 13

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name="Test Manufacturer" + str(manufacturer_id),
                country="Test Country",
            )

    def test_search_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.MANUFACTURER_URL + "?name=Test")
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["name"], "Test"
        )

    def test_manufacturer_queryset_filtered_by_name(self):
        self.client.force_login(self.user)

        Manufacturer.objects.all().delete()

        Manufacturer.objects.create(name="Test name 1", country="Country 1")
        Manufacturer.objects.create(name="Test name 2", country="Country 2")
        Manufacturer.objects.create(name="Another name", country="Country 3")

        response = self.client.get(self.MANUFACTURER_URL + "?name=test name 1")
        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Test name 1")
