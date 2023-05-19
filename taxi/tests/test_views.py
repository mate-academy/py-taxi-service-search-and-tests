from django.contrib.auth import get_user_model
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import TestCase
from django.urls import reverse
from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer, Car


class IndexViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_index_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        Car.objects.create(model="ModelX", manufacturer=manufacturer)
        Car.objects.create(model="Tesla", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 2)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)

    def test_correct_template_index_view_used(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertTemplateUsed(response, "taxi/index.html")

        try:
            get_template("taxi/index.html")
        except TemplateDoesNotExist:
            self.fail("Template 'taxi/index.html' does not exist")


class ManufacturerViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(name="Manufacturer1")
        Manufacturer.objects.create(name="Manufacturer2")
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_manufacturer_create_view(self):
        data = {
            "name": "ManufacturerName",
            "country": "TestCountry"
        }
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(Manufacturer.objects.filter(
            name="ManufacturerName",
            country="TestCountry"
        ).exists()
        )

    def test_manufacturer_delete_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        url = reverse(
            "taxi:manufacturer-delete", kwargs={"pk": manufacturer.pk}
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(pk=manufacturer.pk).exists()
        )
