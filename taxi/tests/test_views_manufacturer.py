from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.forms import ManufacturersSearchForm
from taxi.models import Manufacturer
from taxi.views import ManufacturerListView

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        for number in range(1, 4):
            Manufacturer.objects.create(
                name=f"test{number}",
                country=f"test_country{number}"
            )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self) -> None:

        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertEqual(
            res.context_data["paginator"].num_pages,
            1
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_retrieve_car(self) -> None:
        car = Manufacturer.objects.all()
        res = self.client.get(MANUFACTURER_URL)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(car),
        )
        self.assertEqual(
            res.context_data["paginator"].num_pages,
            1
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_view_context_data(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturersSearchForm
        )

    def test_view_queryset(self) -> None:
        request = self.factory.get(
            MANUFACTURER_URL,
            {"title": "test1"}
        )
        request.user = self.driver
        view = ManufacturerListView()
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(len(queryset), 1)
        self.assertEqual(
            queryset[0].name,
            "test1"
        )
        self.assertEqual(
            queryset[0].country,
            "test_country1"
        )
