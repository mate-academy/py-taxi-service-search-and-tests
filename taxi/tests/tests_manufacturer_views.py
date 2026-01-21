from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer

User = get_user_model()


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


def manufacturer_update_url(pk):
    return reverse("taxi:manufacturer-update", args=[pk])


def manufacturer_delete_url(pk):
    return reverse("taxi:manufacturer-delete", args=[pk])


class PublicManufacturerListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test",
            password="1qazcde3",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)
        for manufacturer in range(7):
            Manufacturer.objects.create(
                name=f"name{manufacturer}", country="country"
            )

    def test_manufacturer_list_status_and_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_context_contains_page_obj_and_paginator(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("page_obj", response.context)
        self.assertIn("paginator", response.context)

    def test_manufacturer_list_pagination_is_5(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?page=2")
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_search_form_in_context_without_query(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial.get("name", ""), "")

    def test_search_form_in_context_with_query(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Toyota")
        form = response.context["search_form"]
        self.assertEqual(form.initial.get("name", "Toyota"), "Toyota")

    def test_correct_list_after_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Toyota")
        expected_qs = Manufacturer.objects.filter(name__icontains="Toyota")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(expected_qs)
        )

    def test_search_is_case_insensitive(self):
        Manufacturer.objects.create(name="TOYOTA", country="Japan")
        Manufacturer.objects.create(name="FORD", country="USA")
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=toyota")
        expected_qs = Manufacturer.objects.filter(name__icontains="toyota")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(expected_qs)
        )

    def test_search_returns_partial_matches(self):
        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        Manufacturer.objects.create(name="Volvo", country="Sweden")
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=vol")
        expected_qs = Manufacturer.objects.filter(name__icontains="vol")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(expected_qs)
        )

    def test_search_with_no_matches_returns_empty_result(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL + "?name=NoMatchWithAnything"
        )
        self.assertFalse(response.context["manufacturer_list"])

    def test_search_results_are_paginated(self):
        for i in range(7):
            Manufacturer.objects.create(
                name=f"Toyota Model {i}", country="Japan"
            )

        response = self.client.get(
            MANUFACTURER_LIST_URL + "?name=Toyota&page=1"
        )
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response_page_2 = self.client.get(
            MANUFACTURER_LIST_URL + "?name=Toyota&page=2"
        )
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response_page_2.context["manufacturer_list"]), 2)

        for manufacturer in response_page_2.context["manufacturer_list"]:
            self.assertIn("Toyota", manufacturer.name)


class PublicManufacturerCreateViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="1qazcde3",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)

    def test_logged_in_and_correct_template(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_create_form_contains_all_fields(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        form = response.context.get("form")
        form_fields = form.fields.keys()
        self.assertIn("name", form_fields)
        self.assertIn("country", form_fields)

    def test_create_manufacturer_success(self):
        data = {"name": "TestName", "country": "TestCountry"}
        count_before = Manufacturer.objects.count()
        response = self.client.post(MANUFACTURER_CREATE_URL, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), count_before + 1)
        manufacturer = Manufacturer.objects.get(name="TestName")
        self.assertEqual(manufacturer.country, "TestCountry")

    def test_error_when_missing_required_fields_on_create(self):
        data = {"name": "TestName", "country": ""}
        count_before = Manufacturer.objects.count()
        response = self.client.post(MANUFACTURER_CREATE_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("country", response.context["form"].errors)
        self.assertEqual(Manufacturer.objects.count(), count_before)


class PublicManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )

    def test_login_required(self):
        url = manufacturer_update_url(self.manufacturer.pk)
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="1qazcde3", license_number="ASD12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )

    def test_login_required(self):
        self.client.logout()
        url = manufacturer_update_url(self.manufacturer.pk)
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_get_update_view_loads_correct_template_and_fills_form(self):
        url = manufacturer_update_url(self.manufacturer.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "taxi/manufacturer_form.html", [t.name for t in response.templates]
        )
        form_initial = response.context["form"].initial
        self.assertEqual(form_initial["name"], self.manufacturer.name)
        self.assertEqual(form_initial["country"], self.manufacturer.country)

    def test_successful_update_redirects_and_changes_data(self):
        url = manufacturer_update_url(self.manufacturer.pk)
        data = {"name": "UpdatedName", "country": "UpdatedCountry"}
        count_before = Manufacturer.objects.count()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, data["name"])
        self.assertEqual(self.manufacturer.country, data["country"])
        self.assertEqual(Manufacturer.objects.count(), count_before)

    def test_update_fails_with_invalid_data(self):
        url = manufacturer_update_url(self.manufacturer.pk)
        data = {"name": "", "country": ""}
        count_before = Manufacturer.objects.count()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "TestName")
        self.assertEqual(self.manufacturer.country, "TestCountry")
        self.assertEqual(Manufacturer.objects.count(), count_before)


class PublicManufacturerDeleteViewTest(TestCase):
    def test_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="DelName", country="DelCountry"
        )
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.pk])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="1qazcde3",
            license_number="ASD12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="DelName", country="DelCountry"
        )

    def test_logged_in_can_access_delete_page(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_confirm_delete.html"
        )

    def test_successful_delete(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.pk])
        count_before = Manufacturer.objects.count()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), count_before - 1)
        with self.assertRaises(Manufacturer.DoesNotExist):
            Manufacturer.objects.get(pk=self.manufacturer.pk)

    def test_delete_nonexistent_object(self):
        url = reverse("taxi:manufacturer-delete", args=[9999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
