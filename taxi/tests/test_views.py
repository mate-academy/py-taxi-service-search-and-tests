from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

DRIVER_LIST_VIEW_URL = reverse("taxi:driver-list")
CAR_LIST_VIEW_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_VIEW_URL = reverse("taxi:manufacturer-list")


class PrivateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer_id=manufacturer.id
        )
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="test_license"
        )
        car.drivers.add(driver)

    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.client.force_login(self.admin)

    def test_drivers_queryset_with_search(self):
        SEARCH_PARAM = "test_"
        response_with_filter = self.client.get(DRIVER_LIST_VIEW_URL, {"username": SEARCH_PARAM})
        drivers_with_filter = get_user_model().objects.filter(username__icontains=SEARCH_PARAM)
        qs_filter = response_with_filter.context.get("driver_list")
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertQuerySetEqual(
            drivers_with_filter,
            qs_filter,
            ordered=False
        )
        self.assertTrue(qs_filter.exists())

    def test_drivers_empty_search(self):
        SEARCH_PARAM = "sth"
        response_with_filter = self.client.get(DRIVER_LIST_VIEW_URL, {"username": SEARCH_PARAM})
        qs_filter = response_with_filter.context.get("driver_list")
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertQuerySetEqual(
            qs_filter,
            [],
            ordered=False
        )
        self.assertFalse(qs_filter.exists())

    def test_cars_queryset_with_search(self):
        SEARCH_PARAM = "test_"
        response_with_filter = self.client.get(CAR_LIST_VIEW_URL, {"model": SEARCH_PARAM})
        cars_with_filter = Car.objects.filter(model__icontains=SEARCH_PARAM)
        qs_filter = response_with_filter.context.get("car_list")
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertQuerySetEqual(
            cars_with_filter,
            qs_filter,
            ordered=False
        )
        self.assertTrue(qs_filter.exists())

    def test_cars_empty_search(self):
        SEARCH_PARAM = "sth"
        response_with_filter = self.client.get(CAR_LIST_VIEW_URL, {"model": SEARCH_PARAM})
        qs_filter = response_with_filter.context.get("car_list")
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertQuerySetEqual(
            qs_filter,
            [],
            ordered=False
        )
        self.assertFalse(qs_filter.exists())

    def test_manufacturers_queryset_with_search(self):
        SEARCH_PARAM = "test_"
        response_with_filter = self.client.get(MANUFACTURER_LIST_VIEW_URL, {"name": SEARCH_PARAM})
        manufacturers_with_filter = Manufacturer.objects.filter(name__icontains=SEARCH_PARAM)
        qs_filter = response_with_filter.context.get("manufacturer_list")
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertQuerySetEqual(
            manufacturers_with_filter,
            qs_filter,
            ordered=False
        )
        self.assertTrue(qs_filter.exists())

    def test_manufacturers_empty_search(self):
        SEARCH_PARAM = "sth"
        response_with_filter = self.client.get(MANUFACTURER_LIST_VIEW_URL, {"name": SEARCH_PARAM})
        qs_filter = response_with_filter.context.get("manufacturer_list")
        self.assertEqual(response_with_filter.status_code, 200)
        self.assertQuerySetEqual(
            qs_filter,
            [],
            ordered=False
        )
        self.assertFalse(qs_filter.exists())

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="test1",
            email="test2",
            password="test3",
            license_number="test4"
        )
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        qs = response.context.get("driver_list")
        self.assertTrue(qs.exists())
        self.assertQuerySetEqual(
            drivers,
            qs,
            ordered=False
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_retrieve_manufacturers(self):
        car = Manufacturer.objects.get(pk=1)
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        qs = response.context.get("manufacturer_list")
        self.assertTrue(qs.exists())
        self.assertQuerySetEqual(
            manufacturers,
            qs,
            ordered=False
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_retrieve_cars(self):
        car = Car.objects.get(pk=1)
        response = self.client.get(CAR_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        qs = response.context.get("car_list")
        self.assertTrue(qs.exists())
        self.assertQuerySetEqual(
            cars,
            qs,
            ordered=False
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )
