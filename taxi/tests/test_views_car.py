from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer
from taxi.views import CarListView

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        for number in range(1, 4):
            Car.objects.create(
                model=f"test{number}",
                manufacturer=Manufacturer.objects.create(
                    name=f"test{number}",
                    country=f"testcountry{number}"
                )
            )
        self.client.force_login(self.driver)

    def test_retrieve_car(self) -> None:
        car = Car.objects.all()
        res = self.client.get(CAR_URL)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(
            list(res.context["car_list"]),
            list(car),
        )
        self.assertEqual(
            res.context_data["paginator"].num_pages,
            1
        )
        self.assertTemplateUsed(
            res,
            "taxi/car_list.html"
        )

    def test_view_context_data(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            CarSearchForm
        )

    def test_view_queryset(self) -> None:
        request = self.factory.get(CAR_URL, {"title": "test1"})
        request.user = self.driver
        view = CarListView()
        view.request = request
        queryset = view.get_queryset()

        self.assertEqual(len(queryset), 1)
        self.assertEqual(
            queryset[0].model,
            "test1"
        )
        self.assertEqual(
            queryset[0].manufacturer.name,
            "test1"
        )
        self.assertEqual(
            queryset[0].manufacturer.country,
            "testcountry1"
        )
