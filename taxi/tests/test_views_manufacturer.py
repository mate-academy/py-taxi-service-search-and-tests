from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class ManufacturerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 7

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Name {manufacturer_id}",
                country=f"Country {manufacturer_id}",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345"
        )
        self.client.force_login(self.user)

        self.list_response = self.client.get(MANUFACTURERS_URL)
        self.create_response = self.client.get(
            reverse("taxi:manufacturer-create"))
        self.update_response = self.client.get(reverse(
            "taxi:manufacturer-update", args=[1]))
        self.delete_response = self.client.get(reverse(
            "taxi:manufacturer-delete", args=[1]))

    def test_manufacturer_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/manufacturers/")
        create_view_response = self.client.get("/manufacturers/create/")
        update_view_response = self.client.get("/manufacturers/3/update/")
        delete_view_response = self.client.get("/manufacturers/6/delete/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)

    def test_manufacturer_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)

    def test_manufacturer_views_uses_correct_template(self):
        self.assertTemplateUsed(
            self.list_response,
            "taxi/manufacturer_list.html")
        self.assertTemplateUsed(
            self.create_response,
            "taxi/manufacturer_form.html")
        self.assertTemplateUsed(
            self.update_response,
            "taxi/manufacturer_form.html")
        self.assertTemplateUsed(
            self.delete_response,
            "taxi/manufacturer_confirm_delete.html")

    def test_manufacturer_list_view_pagination_is_five(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["manufacturer_list"]), 5)

    def test_manufacturer_list_view_lists_all_manufacturers(self):
        response_sec_page = self.client.get(MANUFACTURERS_URL + "?page=2")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["manufacturer_list"]
            ) + list(
                response_sec_page.context["manufacturer_list"]
            ), list(manufacturers))

    def test_manufacturer_list_view_search(self):
        number_of_manufacturers = 7
        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Manuf {manufacturer_id}",
                country=f"Country {manufacturer_id}",
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                MANUFACTURERS_URL + "?name=Manuf" + f"&page={page_number}",
            )
            response_list += list(search_result.context["manufacturer_list"])
        filter_result = Manufacturer.objects.filter(
            name__icontains="Manuf"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_manufacturer_create_view_creates_manufacturer(self):
        form_data = {
            "name": "Kraz",
            "country": "Ukraine"
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_manufacturer_update_view_updates_manufacturer(self):
        form_data = {
            "name": "Opel",
            "country": "Germany"
        }
        manufacturer_id_for_update = Manufacturer.objects.get(name="Name 1").id
        self.client.post(reverse(
            "taxi:manufacturer-update",
            args=[manufacturer_id_for_update]),
            data=form_data)
        updated_manufacturer = Manufacturer.objects.get(
            id=manufacturer_id_for_update)

        self.assertEqual(updated_manufacturer.name, form_data["name"])
        self.assertEqual(updated_manufacturer.country, form_data["country"])

    def test_manufacturer_delete_view_deletes_manufacturer(self):
        manufacturer_id_for_delete = Manufacturer.objects.get(name="Name 1").id
        self.client.post(reverse(
            "taxi:manufacturer-delete",
            args=[manufacturer_id_for_delete]))

        self.assertEqual(list(Manufacturer.objects.filter(name="Name 1")), [])
