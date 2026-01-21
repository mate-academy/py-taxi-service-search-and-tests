from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver


class LoginTest(TestCase):
    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class ViewTestPrivate(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="Vasavik", password="password"
        )
        Manufacturer.objects.create(
            name="Opel",
            country="Dauchland"
        )
        self.client.force_login(self.user)

    def test_existing_url_manufacturers(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_correct_template_use(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_form_in_context(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial,
            {"name": ""}
        )
