from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


MANUFACTURER_FORMATS_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerFormatTests(TestCase):
    def test_login_requirement_list(self):
        res_list = self.client.get(MANUFACTURER_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login_requirement_create(self):
        res_create = self.client.get(MANUFACTURER_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_update_delete_without_login(self):

        manufacturer = Manufacturer.objects.create(
                name="BMW",country="Germany",
            )
        url_1 = reverse('taxi:manufacturer-update', kwargs={'pk': manufacturer.pk})
        url_2 = reverse('taxi:manufacturer-delete', kwargs={'pk': manufacturer.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivateManufacturerFormatTests(TestCase):

    def setUp(self) -> None:
        number_of_manufactory = 7

        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        for manufactory_id in range(number_of_manufactory):
            Manufacturer.objects.create(
                name=f"BMW{manufactory_id}",
                country=f"Germany{manufactory_id}",
            )

    def test_retrieve_manufacturer(self):

        response = self.client.get(MANUFACTURER_FORMATS_URL +"?page=1")
        response_2 = self.client.get(MANUFACTURER_FORMATS_URL + "?page=2")
        manufacturer = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["manufacturer_list"])
             + list(response_2.context["manufacturer_list"])
             )
            ,list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_update_delete_manufactory_wit_login(self):

        manufacturer = Manufacturer.objects.first()
        url_1 = reverse('taxi:manufacturer-update', kwargs={'pk': manufacturer.pk})
        url_2 = reverse('taxi:manufacturer-delete', kwargs={'pk': manufacturer.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEquals(res_1.status_code, 200)
        self.assertEquals(res_2.status_code, 200)


    def test_if_search_name_is_a_character_w1(self):
        response = self.client.get(MANUFACTURER_FORMATS_URL +"?name=w1")
        manufacturer = Manufacturer.objects.filter(
            name__icontains="w1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),list(manufacturer)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(response.context["search_form"].initial["name"], "w1")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEquals(response.status_code, 200)


    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_FORMATS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['manufacturer_list']), 5)

    def test_pagination_is_second_page_five(self):
        response = self.client.get(MANUFACTURER_FORMATS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['manufacturer_list']), 2)

    def test_create_success_url_is_with_redict_to_list(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(MANUFACTURER_CREATE_URL, {"name":"BMW", "country": "German"})
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_update_success_url_is_with_redict_to_list(self):
        response = reverse('taxi:manufacturer-update', kwargs={'pk': 1})

        response = self.client.post(response, {"name":"Test", "country": "Ukraine"})
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEquals(str(manufacturer), "Test Ukraine")
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

