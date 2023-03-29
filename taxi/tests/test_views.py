from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer
from taxi.urls import urlpatterns
from taxi.views import ManufacturerListView


class PublicAccessTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url_names = [url for url in urlpatterns if hasattr(url, "name")]

    def test_login_required_for_anonymous_user(self):
        for url in self.url_names:
            if "<int:pk>" in str(url):
                valid_url = reverse(f"taxi:{url.name}", kwargs={"pk": 1})
            else:
                valid_url = reverse(f"taxi:{url.name}")

            with self.subTest(url=url):
                res = self.client.get(valid_url)
                self.assertNotEqual(res.status_code, 200)


class ManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser", password="123456789"
        )

        for i in range(5):
            Manufacturer.objects.create(
                name=f"Manufacturer{i}", country=f"Country{i}"
            )

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-list")
        self.response = self.client.get(self.url)

    def test_context_has_search_form(self):
        context = self.client.get(self.url).context
        self.assertIn("search_form", context)

    def test_queryset_with_search_criteria(self):
        filtered_manufacturer_list = Manufacturer.objects.filter(
            name__icontains=2
        )
        non_filtered_manufacturer_list = Manufacturer.objects.all()

        response_add_criteria = self.client.get(
            self.url + "?search_criteria=2"
        )
        response_empty_criteria = self.client.get(
            self.url + "?search_criteria="
        )

        self.assertEqual(
            list(response_add_criteria.context.get("manufacturer_list")),
            list(filtered_manufacturer_list),
        )

        self.assertEqual(
            list(response_empty_criteria.context.get("manufacturer_list")),
            list(non_filtered_manufacturer_list),
        )
