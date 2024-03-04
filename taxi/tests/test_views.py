from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")
LOGIN_URL = reverse("login")


class UnregisteredUserTest(TestCase):

    def test_login_required_manufacturer_list_page(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_list_page(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_list_page(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_index_page(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_can_get_to_login_page(self):
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_search_field_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        expected_query_set = Manufacturer.objects.filter(
            name__icontains="TestName"
        )

        response = self.client.get(MANUFACTURER_LIST_URL + "?name=TestName")
        result_query_set = response.context_data["manufacturer_list"]

        self.assertEqual(
            list(expected_query_set),
            list(result_query_set)
        )


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        Car.objects.create(
            model="X5", manufacturer=bmw
        )
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        models = ["TestModel_1", "TestModel_2", "TestModel_3"]
        for i in range(3):
            Car.objects.create(
                model=models,
                manufacturer=manufacturer
            )

        response = self.client.get(CAR_LIST_URL + "?model=TestModel")

        expected_query_set = Car.objects.filter(model__icontains="TestModel")

        result_query_set = response.context_data["car_list"]

        self.assertEqual(
            list(expected_query_set),
            list(result_query_set)
        )


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_search_driver_by_username(self):

        usernames = ["example_user_1", "user_2", "example_user_3"]
        passwords = ["Password_1", "Password_2", "Password_3"]
        license_numbers = ["EXA11111", "EXA22222", "EXA33333"]

        for i in range(3):
            get_user_model().objects.create(
                username=[usernames[i]],
                password=[passwords[i]],
                license_number=[license_numbers[i]]
            )

        expected_query_set = get_user_model().objects.filter(
            username__icontains="example"
        )

        response = self.client.get(DRIVER_LIST_URL + "?username=example")
        self.assertEqual(response.status_code, 200)

        response_query_set = response.context_data["driver_list"]

        self.assertEqual(
            list(response_query_set),
            list(expected_query_set)
        )
