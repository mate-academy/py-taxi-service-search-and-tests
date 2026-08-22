from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345"
        )
        self.url = reverse("taxi:manufacturer-list")

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_uses_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_by_name(self):
        skoda = Manufacturer.objects.create(name="Skoda",
                                            country="Czech Republic")
        bmw = Manufacturer.objects.create(name="BMW",
                                          country="Germany")
        audi = Manufacturer.objects.create(name="Audi",
                                           country="Germany")

        self.client.force_login(self.user)

        response = self.client.get(self.url, {"name": "bmw"})

        manufacturers = response.context["manufacturer_list"]

        self.assertIn(bmw, manufacturers)
        self.assertEqual(manufacturers.count(), 1)
        self.assertNotIn(skoda, manufacturers)
        self.assertNotIn(audi, manufacturers)

    def test_without_search_returns_all_manufacturers(self):
        skoda = Manufacturer.objects.create(name="Skoda",
                                            country="Czech Republic")
        bmw = Manufacturer.objects.create(name="BMW",
                                          country="Germany")
        audi = Manufacturer.objects.create(name="Audi",
                                           country="Germany")

        self.client.force_login(self.user)

        response = self.client.get(self.url)

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(manufacturers.count(), 3)
        self.assertIn(skoda, manufacturers)
        self.assertIn(bmw, manufacturers)
        self.assertIn(audi, manufacturers)

    def test_pagination(self):
        self.client.force_login(self.user)
        for i in range(6):
            Manufacturer.objects.create(name=f"BMW{i}",
                                        country="Germany")

        response = self.client.get(self.url)

        manufacturers = response.context["manufacturer_list"]
        page_obj = response.context["page_obj"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(manufacturers.count(), 5)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertEqual(page_obj.number, 1)
        self.assertEqual(page_obj.paginator.num_pages, 2)


class TestManufacturerCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345",
        )
        self.url = reverse("taxi:manufacturer-create")

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_successful_creation_manufacturer(self):
        self.client.force_login(self.user)

        self.assertEqual(Manufacturer.objects.count(), 0)

        response = self.client.post(self.url, {"name": "BMW",
                                               "country": "Germany"})
        manufacturer = Manufacturer.objects.get(name="BMW")

        self.assertTrue(Manufacturer.objects.filter(
            name="BMW",
            country="Germany", ).exists())
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(Manufacturer.objects.count(), 1)
        self.assertEqual(manufacturer.name, "BMW")
        self.assertEqual(manufacturer.country, "Germany")

    def test_invalid_data_does_not_create_manufacturer(self):
        self.client.force_login(self.user)

        self.assertEqual(Manufacturer.objects.count(), 0)

        response = self.client.post(self.url, {"name": "", "country": ""}, )
        form = response.context["form"]

        self.assertEqual(Manufacturer.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())


class TestManufacturerUpdateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )
        self.manufacturer = Manufacturer.objects.create(name="BMW",
                                                        country="Germany", )
        self.url = reverse("taxi:manufacturer-update",
                           kwargs={"pk": self.manufacturer.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_updating_existing_manufacturer(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"name": "BMW",
                                               "country": "Finland"})

        self.manufacturer.refresh_from_db()

        self.assertEqual(self.manufacturer.name, "BMW")
        self.assertEqual(self.manufacturer.country, "Finland")
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_invalid_data_does_not_change_manufacturer(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"name": "",
                                               "country": ""})
        form = response.context["form"]
        self.manufacturer.refresh_from_db()

        self.assertFalse(form.is_valid())
        self.assertEqual(self.manufacturer.name, "BMW")
        self.assertEqual(self.manufacturer.country, "Germany")
        self.assertEqual(response.status_code, 200)


class TestManufacturerDeleteView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )
        self.manufacturer = Manufacturer.objects.create(name="Audi",
                                                        country="Germany", )

        self.url = reverse("taxi:manufacturer-delete",
                           kwargs={"pk": self.manufacturer.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_deleting_manufacturer(self):
        self.client.force_login(self.user)
        self.assertEqual(Manufacturer.objects.count(), 1)

        response = self.client.post(self.url)

        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer.pk).exists()
        )
        self.assertEqual(Manufacturer.objects.count(), 0)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
