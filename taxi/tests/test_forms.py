from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car
from taxi.tests.test_views import(
    MANUFACTURER_LIST_URL,
    CAR_LIST_URL,
    DRIVER_LIST_URL,
)


class SearchManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota Trucks", country="Japan")

        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})

        self.assertEqual(response.status_code, 200)

        expected_manufacturers = Manufacturer.objects.filter(
            name__icontains="Toyota"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(expected_manufacturers),
        )


class SearchCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        Car.objects.create(model="test_model", manufacturer=manufacturer)
        Car.objects.create(model="test_model2", manufacturer=manufacturer)
        Car.objects.create(model="model_test3", manufacturer=manufacturer)

        response = self.client.get(CAR_LIST_URL, {"model": "test_model"})

        self.assertEqual(response.status_code, 200)

        expected_cars = Car.objects.filter(
            model__icontains="test_model"
        )
        self.assertEqual(
            list(response.context["car_list"]),
            list(expected_cars),
        )


class SearchDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):

        Driver.objects.create(
            username="user_test",
            password="test123",
            license_number="test_license123"
        )
        Driver.objects.create(
            username="user_test2",
            password="test234",
            license_number="test_license234"
        )
        Driver.objects.create(
            username="test_username3",
            password="test345",
            license_number="test_license345"
        )

        response = self.client.get(DRIVER_LIST_URL, {"username": "user_test"})

        self.assertEqual(response.status_code, 200)

        expected_drivers = Driver.objects.filter(
            username__icontains="user_test"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(expected_drivers),
        )