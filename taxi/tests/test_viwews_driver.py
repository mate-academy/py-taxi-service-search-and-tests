from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Driver
from taxi.views import DriverListView

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        for number in range(1, 4):
            Driver.objects.create(
                username=f"test{number}",
                password=f"test{number}",
                first_name=f"test{number}",
                last_name=f"test{number}",
                license_number=f"ASD123{number}",
            )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self) -> None:

        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers),
        )
        self.assertEqual(
            res.context_data["paginator"].num_pages,
            1
        )
        self.assertTemplateUsed(
            res,
            "taxi/driver_list.html"
        )

    def test_view_context_data(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )

    def test_view_queryset(self) -> None:
        request = self.factory.get(
            DRIVER_URL,
            {"title": "test1"}
        )
        request.user = self.driver
        view = DriverListView()
        view.request = request
        queryset = view.get_queryset()

        self.assertEqual(len(queryset), 1)
        self.assertEqual(
            queryset[0].first_name,
            "test1"
        )
        self.assertEqual(
            queryset[0].last_name,
            "test1"
        )
        self.assertEqual(
            queryset[0].license_number,
            "ASD1231"
        )
