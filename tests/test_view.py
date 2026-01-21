from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView, CarListView


class ManufacturerTestCase(TestCase):
    def setUp(self):
        name = "BMW"
        country = "Germany"
        self.manufacturer = Manufacturer.objects.create(name=name, country=country)

        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD>",
        )

        self.factory = RequestFactory()
        self.view = ManufacturerListView()

    def test_context_data(self):
        self.client.login(username="admin", password="<PASSWORD>")
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertIn("search_form", res.context)

    def test_queryset_with_get(self):
        self.client.login(username="admin", password="<PASSWORD>")
        request = self.factory.get("manufacturers/?model=B")
        self.view.request = request
        model = Manufacturer.objects.filter(name__icontains="B")

        queryset = self.view.get_queryset()
        true_quryset = model
        self.assertEqual(list(queryset), list(true_quryset))


class CarTestCase(TestCase):
    def setUp(self):
        name = "BMW"
        country = "Germany"
        self.manufacturer = Manufacturer.objects.create(name=name, country=country)
        username = "Admin"
        password = "<PASSWORD>"
        license_number = "LAT12345"
        first_name = "John"
        last_name = "Doe"
        self.driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
        )
        self.car = Car.objects.create(
            model="X6",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])
        self.factory = RequestFactory()
        self.view = CarListView()

    def test_context_data(self):
        self.client.login(username="Admin", password="<PASSWORD>")
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertIn("search_form", res.context)

    def test_queryset_with_get(self):
        self.client.login(username="Admin", password="<PASSWORD>")
        request = self.factory.get("cars/?model=x")
        self.view.request = request
        model = Car.objects.filter(model__icontains="x")

        queryset = self.view.get_queryset()
        true_quryset = model
        self.assertEqual(list(queryset), list(true_quryset))


class DriversTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD>",
        )

        self.factory = RequestFactory()
        self.view = ManufacturerListView()

    def test_context_data(self):
        self.client.login(username="admin", password="<PASSWORD>")
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertIn("search_form", res.context)

    def test_queryset_with_get(self):
        self.client.login(username="admin", password="<PASSWORD>")
        request = self.factory.get("drivers/?username=a")
        self.view.request = request
        model = get_user_model().objects.filter(username__icontains="B")

        queryset = self.view.get_queryset()
        true_quryset = model
        self.assertEqual(list(queryset), list(true_quryset))
