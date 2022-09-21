from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from taxi.models import Manufacturer
from taxi.views import ManufacturerListView

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class ManufacturerTest(TestCase):

    def setUp(self):
        num_manuf = 8
        for manuf_id in range(num_manuf):
            Manufacturer.objects.create(name=f"Test_{manuf_id}", country=f"State_{manuf_id}")

        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="driver1234"
        )

        self.client.force_login(self.user)

    def test_public_login_required(self):
        self.client.logout()
        resp = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)
        self.assertRedirects(resp, "/accounts/login/?next=/manufacturers/")

    def test_retrieve_manufacturer_list_pagination_5(self):
        resp = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")
        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertTrue(len((resp.context["manufacturer_list"])) == 5)

    def test_pagination_second_page(self):
        resp = self.client.get(MANUFACTURER_LIST_URL + "?page=2")

        self.assertEqual(len(resp.context["manufacturer_list"]), 3)

    def test_update_delete_link(self):
        manuf = Manufacturer.objects.get(id=1)
        resp = self.client.get(reverse("taxi:manufacturer-update", kwargs={"pk": manuf.id}))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_form.html")

        resp = self.client.get(reverse("taxi:manufacturer-delete", kwargs={"pk": manuf.id}))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_confirm_delete.html")

    def test_search_queryset_manufacturer(self):
        request = RequestFactory().get("?name=Test_manufacturer")
        view = ManufacturerListView()
        view.request = request
        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Manufacturer.objects.filter(name__icontains="Test_manufacturer"))
