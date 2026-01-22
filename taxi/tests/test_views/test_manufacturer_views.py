from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

Driver = get_user_model()

LIST_VIEW_URL = reverse("taxi:manufacturer-list")


class ManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturers_count = 8

        Driver.objects.create_user(
            username="Username",
            password="test_password",
            license_number="AAA12345"
        )

        for manufacturer_copy in range(cls.manufacturers_count):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_copy}",
                country=f"Country {manufacturer_copy}",
            )

    def test_login_required(self):
        response = self.client.get(LIST_VIEW_URL)
        self.assertRedirects(
            response,
            reverse("login") + f"?next={LIST_VIEW_URL}"
        )

    def test_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_context_object_name(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertIn(
            "manufacturer_list",
            response.context
        )

    def test_paginated_by_5(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response = self.client.get(LIST_VIEW_URL + "?page=2")
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_model(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        for manufacturer in response.context["manufacturer_list"]:
            self.assertIsInstance(manufacturer, Manufacturer)

    def test_search_form_in_context(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )

    def test_search_form_use_apply_name_param(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?name=4")

        self.assertEqual(
            response.context["search_form"].initial["name"],
            "4"
        )

        self.assertEqual(
            len(response.context["manufacturer_list"]),
            1
        )
        self.assertContains(
            response,
            "Manufacturer 4"
        )

    def test_search_form_check_for_contains(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?name=FACT")

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            Manufacturer.objects.filter(name__icontains="FACT").count()
        )

    def test_has_update_and_delete_anchors(self):
        manufacturers = Manufacturer.objects.all()[:5]
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        for manufacturer in manufacturers:
            update_url = reverse(
                "taxi:manufacturer-update",
                args=[manufacturer.id]
            )
            self.assertContains(
                response,
                f'href="{update_url}"'
            )
            delete_url = reverse(
                "taxi:manufacturer-delete",
                args=[manufacturer.id]
            )

            self.assertContains(
                response,
                f'href="{delete_url}"'
            )

    def test_returns_nothing_for_bad_search(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?name=bad_search_param")

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            0
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            0
        )


CREATE_VIEW_URL = reverse("taxi:manufacturer-create")


class ManufacturerCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="Username",
            password="test_password",
            license_number="AAA12345"
        )

    def test_login_required(self):
        response = self.client.get(CREATE_VIEW_URL)
        self.assertRedirects(
            response,
            reverse("login") + f"?next={CREATE_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(CREATE_VIEW_URL)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_form.html"
        )

    def test_creates_new_object(self):
        self.client.force_login(Driver.objects.get(pk=1))
        manufacturer_data = {
            "name": "Manufacturer",
            "country": "Country"
        }
        response = self.client.post(
            CREATE_VIEW_URL,
            manufacturer_data
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

        manufacturer = list(
            Manufacturer.objects.filter(
                name=manufacturer_data["name"]
            ).values("name", "country")
        )

        self.assertEqual(
            manufacturer,
            [manufacturer_data]
        )

    def test_should_not_create_if_data_is_invalid(self):
        self.client.force_login(Driver.objects.get(pk=1))
        manufacturer_data = {}
        response = self.client.post(
            CREATE_VIEW_URL,
            manufacturer_data
        )

        self.assertEqual(
            response.context["form"].errors,
            {
                "name": ["This field is required."],
                "country": ["This field is required."]
            }
        )

        manufacturer_data = {
            "name": "Manufacturer",
            "country": "Country"
        }

        self.client.post(
            CREATE_VIEW_URL,
            manufacturer_data
        )
        response = self.client.post(
            CREATE_VIEW_URL,
            manufacturer_data
        )

        self.assertEqual(
            response.context["form"].errors,
            {
                "name": ["Manufacturer with this Name already exists."],
            }
        )


UPDATE_VIEW_URL = reverse(
    "taxi:manufacturer-update",
    args=[1]
)


class ManufacturerUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="Username",
            password="test_password",
            license_number="AAA12345"
        )

        manufactures_count = 2
        for manufacture_copy in range(manufactures_count):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacture_copy}",
                country=f"Country {manufacture_copy}"
            )

    def test_login_required(self):
        response = self.client.get(
            UPDATE_VIEW_URL
        )
        self.assertRedirects(
            response,
            reverse("login")
            + f"?next={UPDATE_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            UPDATE_VIEW_URL
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_form.html"
        )

    def test_show_data_from_manufacturer(self):
        self.client.force_login(Driver.objects.get(pk=1))
        manufacturer = Manufacturer.objects.get(pk=1)

        response = self.client.get(
            UPDATE_VIEW_URL
        )

        self.assertContains(
            response,
            f'value="{manufacturer.name}"'
        )

        self.assertContains(
            response,
            f'value="{manufacturer.country}"'
        )

    def test_updates_object(self):
        self.client.force_login(Driver.objects.get(pk=1))

        manufacturers_before = list(
            Manufacturer.objects.all().values("name", "country")
        )

        manufacturers_before[0]["name"] = "Manufacturer 0"

        response = self.client.post(
            UPDATE_VIEW_URL,
            manufacturers_before[0]
        )
        self.assertRedirects(response, LIST_VIEW_URL)

        manufacturers_after = list(
            Manufacturer.objects.all().values("name", "country")
        )

        self.assertEqual(
            manufacturers_before,
            manufacturers_after
        )

    def test_should_not_update_if_data_is_invalid(self):
        self.client.force_login(Driver.objects.get(pk=1))

        response = self.client.post(
            UPDATE_VIEW_URL,
            {}
        )

        self.assertEqual(
            response.context["form"].errors,
            {
                "name": ["This field is required."],
                "country": ["This field is required."]
            }
        )

        manufacturer_data = {
            "name": "Manufacturer 2",
            "country": "Country"
        }

        self.client.post(
            CREATE_VIEW_URL,
            manufacturer_data
        )
        response = self.client.post(
            CREATE_VIEW_URL,
            manufacturer_data
        )

        self.assertEqual(
            response.context["form"].errors,
            {
                "name": ["Manufacturer with this Name already exists."],
            }
        )


DELETE_VIEW_URL = reverse(
    "taxi:manufacturer-delete",
    args=[1]
)


class ManufacturerDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="Username",
            password="test_password",
            license_number="AAA12345"
        )

        manufactures_count = 2
        for manufacture_copy in range(manufactures_count):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacture_copy}",
                country=f"Country {manufacture_copy}"
            )

    def test_login_required(self):
        response = self.client.get(
            DELETE_VIEW_URL
        )
        self.assertRedirects(
            response,
            reverse("login")
            + f"?next={DELETE_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            DELETE_VIEW_URL
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_deletes_only_selected_manufacturer(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.post(
            DELETE_VIEW_URL
        )

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(Manufacturer.objects.filter(pk=1).count(), 0)
        self.assertEqual(Manufacturer.objects.count(), 1)

    def test_show_404_for_invalid_id(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[123])
        )

        self.assertEqual(response.status_code, 404)
