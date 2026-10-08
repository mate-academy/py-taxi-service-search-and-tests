from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer, Car, Driver


class SearchManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345"
        )
        manufacturers_to_create = [
            Manufacturer(name="BMW", country="Germany"),
            Manufacturer(name="Bugatti", country="France"),
            Manufacturer(name="Bentley", country="United Kingdom"),
        ]
        Manufacturer.objects.bulk_create(manufacturers_to_create)

    def test_search_manufacturers(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"search_query": "b"}
        )
        expected_queryset = Manufacturer.objects.filter(
            name__icontains="b"
        )
        self.assertQuerySetEqual(
            response.context["manufacturer_list"],
            expected_queryset,
            ordered=False
        )


class SearchCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345",
            license_number="TES12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Bugatti",
            country="France"
        )

        car_1 = Car.objects.create(
            model="Veyron",
            manufacturer=self.manufacturer
        )
        car_2 = Car.objects.create(
            model="Chiron",
            manufacturer=self.manufacturer
        )
        car_3 = Car.objects.create(
            model="Tourbillon",
            manufacturer=self.manufacturer
        )

        car_1.drivers.add(self.user)
        car_2.drivers.add(self.user)
        car_3.drivers.add(self.user)

    def test_search_cars(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"search_query": "on"}
        )
        expected_queryset = Car.objects.filter(
            model__icontains="on"
        )
        self.assertQuerySetEqual(
            response.context["car_list"],
            expected_queryset,
            ordered=False
        )


class SearchDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_search_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"search_query": "user"}
        )
        expected_queryset = Driver.objects.filter(
            username__icontains="user"
        )
        self.assertQuerySetEqual(
            response.context["driver_list"],
            expected_queryset,
            ordered=False
        )


class TestCreateDriver(TestCase):
    def test_create_driver_form_is_valid(self):
        form_data = {
            "username": "test_user_2",
            "license_number": "TES12345",
            "password1": "someletters12345",
            "password2": "someletters12345",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestCreateCar(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_create_car_form_is_valid(self):
        driver_1 = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345",
            license_number="TES12345"
        )
        driver_2 = get_user_model().objects.create_user(
            username="test_user_2",
            password="password12345",
            license_number="TES67890"
        )
        driver_3 = get_user_model().objects.create_user(
            username="test_user_3",
            password="password12345",
            license_number="TES09876"

        )
        form_data = {
            "model": "test_model",
            "manufacturer": self.manufacturer.id,
            "drivers": (driver_1, driver_2, driver_3)
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestDriverList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345"
        )

    def test_driver_list_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:driver-list")
        )
        self.assertEqual(response.status_code, 200)


class TestManufacturerList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345"
        )

    def test_manufacturer_list_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertEqual(response.status_code, 200)


class TestCarList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_1",
            password="password12345"
        )

    def test_car_list_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertEqual(response.status_code, 200)
