from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.views import CarListView, DriverListView

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")
CARS_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicManufacturersTests(TestCase):
    def test_login_not_required(self):
        response_ = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertNotEqual(response_.status_code, 200)


class PrivateManufacturersTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin11",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Test Name 1",
            country="Test Country 1"
        )
        self.manufacturer_3 = Manufacturer.objects.create(
            name="Name 1",
            country="Test Country 2"
        )

    def test_login_required(self):
        response_ = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertEqual(response_.status_code, 200)

    def test_retrieve_manufacturers_list(self):
        response_ = self.client.get(MANUFACTURERS_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response_.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response_, "taxi/manufacturer_list.html")

    def test_get_queryset(self):
        manufacturers = Manufacturer.objects.filter(name__icontains="test")
        response_ = self.client.get(MANUFACTURERS_LIST_URL + "?name=test")

        self.assertEqual(
            list(response_.context["manufacturer_list"]),
            list(manufacturers)
        )


class PrivateCarTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin11",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )

        for index in range(5):
            Car.objects.create(
                model=f"Test model-{index}",
                manufacturer=self.manufacturer,
            )
        self.different_car = Car.objects.create(
            model="Different car",
            manufacturer=self.manufacturer,
        )

    def test_login_required(self):
        response_ = self.client.get(CARS_LIST_URL)

        self.assertEqual(response_.status_code, 200)

    def test_retrieve_paginated_car_list(self):
        response_ = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()
        pagination = CarListView.paginate_by

        self.assertEqual(
            list(response_.context["car_list"]),
            list(cars)[:pagination]
        )
        self.assertTemplateUsed(response_, "taxi/car_list.html")

    def test_get_queryset(self):
        manufacturers = Car.objects.filter(model__icontains="test")
        response_ = self.client.get(CARS_LIST_URL + "?model=test")

        self.assertEqual(
            list(response_.context["car_list"]),
            list(manufacturers)
        )


class DriverTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin11",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="test first",
            last_name="test last",
            password="test1234",
            license_number="ABC12346"
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set = [self.driver.pk]

    def test_login_required(self):
        response_ = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response_.status_code, 200)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "first_name": "test first",
            "password1": "driver123",
            "password2": "driver123",
            "last_name": "test last",
            "license_number": "ABC12346"}

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_retrieve_paginated_car_list(self):
        response_ = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()
        pagination = DriverListView.paginate_by

        self.assertEqual(
            list(response_.context["driver_list"]),
            list(drivers)[:pagination]
        )
        self.assertTemplateUsed(response_, "taxi/driver_list.html")

    def test_get_queryset(self):
        drivers = get_user_model().objects.filter(username__icontains="test")
        response_ = self.client.get(DRIVER_LIST_URL + "?username=test")

        self.assertEqual(
            list(response_.context["driver_list"]),
            list(drivers)
        )
