from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.views import CarListView

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        resp = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(resp.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test3",
            password="password3"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="man1",
            country="count1"
        )
        Manufacturer.objects.create(
            name="man2",
            country="count2"
        )
        self.resp = self.client.get(MANUFACTURER_URL)

    def test_retrieve_manufacturers(self):
        self.assertEqual(self.resp.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(self.resp.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_check_template_manufacturers(self):
        self.assertTemplateUsed(
            self.resp, "taxi/manufacturer_list.html"
        )


class SearchCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test3",
            password="password3"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="man1",
            country="count1"
        )
        username = "test"
        password = "test1111"
        license_number = "12345678"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        cars = Car.objects.bulk_create([
            Car(
                model="m1",
                manufacturer=manufacturer
            ),
            Car(
                model="m2",
                manufacturer=manufacturer,
            )
        ])
        [car.drivers.set([driver]) for car in cars]

        self.factory = RequestFactory()

    def test_search_car_one_result(self):
        test_data = "1"
        request = self.factory.get(CAR_URL, {"model": test_data})
        request.user = self.user

        view = CarListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        queryset = response.context_data["object_list"]
        self.assertEqual(queryset.count(), 1)
        self.assertQuerysetEqual(
            queryset, Car.objects.filter(model__icontains=test_data)
        )

    def test_search_car_no_result(self):
        test_data = "$$$"
        request = self.factory.get(CAR_URL, {"model": test_data})
        request.user = self.user

        view = CarListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        queryset = response.context_data["object_list"]
        self.assertEqual(queryset.count(), 0)
        self.assertQuerysetEqual(
            queryset, Car.objects.filter(model__icontains=test_data)
        )

    def test_search_car_all_result(self):
        test_data = ""
        request = self.factory.get(CAR_URL, {"model": test_data})
        request.user = self.user

        view = CarListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        queryset = response.context_data["object_list"]
        self.assertEqual(queryset.count(), 2)
        self.assertQuerysetEqual(
            queryset,
            Car.objects.filter(model__icontains=test_data),
            ordered=False
        )
