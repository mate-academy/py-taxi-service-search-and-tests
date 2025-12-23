from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.manufacturer.save()

        self.urls_list = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.id}
            ),
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.id}
            ),
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.urls_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="Test123",
        )
        self.user.save()
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.manufacturer1.save()

        self.manufacturer2 = Manufacturer.objects.create(
            name="Other Manufacturer",
            country="Other Country",
        )
        self.manufacturer2.save()

        self.urls_list = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer1.id}
            ),
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer1.id}
            ),
        ]

        self.response_list = [self.client.get(url) for url in self.urls_list]

        self.templates_list = [
            "taxi/manufacturer_list.html",
            "taxi/manufacturer_form.html",
            "taxi/manufacturer_confirm_delete.html",
            "taxi/manufacturer_form.html",
        ]

        self.manufacturer_list_url = reverse("taxi:manufacturer-list")
        self.manufacturer_list_response = self.client.get(
            self.manufacturer_list_url
        )

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_manufacturer(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(self.manufacturer_list_response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_manufacturer(self):
        search_manufacturer = Manufacturer.objects.filter(
            name__icontains="Test"
        )
        search_manufacturer_response = self.client.get(
            self.manufacturer_list_url + "?name=Test"
        )
        self.assertEqual(
            list(search_manufacturer),
            list(search_manufacturer_response.context["manufacturer_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
