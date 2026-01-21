from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Driver


class ManufacturerListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="testuser", password="password")
        cls.manufacturers = [
            Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country=f"Country {i}") for i in range(15)
        ]

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="password")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_database_content(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers.count(), 15)
        for i in range(15):
            self.assertTrue(Manufacturer.objects.filter(
                name=f"Manufacturer {i}").exists())

    def test_response_context(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_list_displays_first_five_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_names = [f"Manufacturer {i}" for i in range(5)]
        for name in manufacturer_names:
            self.assertContains(response, name)

    def test_pagination_second_page(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?page=2")
        manufacturer_names = [f"Manufacturer {i}" for i in range(5, 10)]
        for name in manufacturer_names:
            self.assertContains(response, name)

    def test_pagination_third_page(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?page=3")
        manufacturer_names = [f"Manufacturer {i}" for i in range(10, 15)]
        for name in manufacturer_names:
            self.assertContains(response, name)
