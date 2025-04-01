from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import SingleFieldSearchForm
from taxi.models import Manufacturer

User = get_user_model()
MANUFACTURER_CREATE = reverse("taxi:manufacturer-create")
MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
MANUFACTURER_DETAIL = reverse("taxi:manufacturer-detail", kwargs={"pk": 1})
MANUFACTURER_UPDATE = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})

URL_LIST = [
    MANUFACTURER_CREATE,
    MANUFACTURER_LIST,
    MANUFACTURER_DETAIL,
    MANUFACTURER_UPDATE,
    MANUFACTURER_DELETE
]


class PublicManufacturerTest(TestCase):
    def test_login_requirement_url(self):
        """
        Test that unauthorized user can't get access any manufacturer page
        """
        for url in URL_LIST:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)
                self.assertIn("/accounts/login/", response.url)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

    def test_authorized_user_manufacturer_url(self):
        """
            Test that authorized user get access any manufacturer page
        """
        for url in URL_LIST:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_manufacturer_create_post_success_url(self):
        """
        Test that create new manufacturer get back page to redirect
        """
        back_url = "/taxi/manufacturers/"
        url = reverse("taxi:manufacturer-create") + f"?back={back_url}"
        response = self.client.post(
            url,
            data={"name": "test_model", "country": "test_country"}
        )
        self.assertRedirects(response, back_url)
        self.assertTrue(Manufacturer.objects.filter(
            name="test_model"
        ).exists())

    def test_create_redirects_to_default_if_no_back(self):
        """
        Test that create new manufacturer back to manufacturer list if no back
        """
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(
            url,
            data={"name": "Audi", "country": "Germany"}
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_get_context_data(self):
        """
        Test that search_form exists in context
        and contains correct initial data
        """
        response = self.client.get(MANUFACTURER_LIST + "?query=test_query")
        self.assertIn("search_form", response.context)

        form = response.context["search_form"]
        self.assertIsInstance(form, SingleFieldSearchForm)
        self.assertEqual(form.initial["query"], "test_query")

    def test_manufacturer_get_queryset_without_query(self):
        """
        Test search without parameters. Default query
        """
        response = self.client.get(MANUFACTURER_LIST)
        object_list = response.context["object_list"]
        self.assertEqual(set(object_list), set(Manufacturer.objects.all()))

    def test_manufacturer_get_queryset_with_query(self):
        """
            Test search without parameters. Default with parameters
        """
        response = self.client.get(MANUFACTURER_LIST + "?query=BMW")
        object_list = response.context["object_list"]
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].name, "BMW")
