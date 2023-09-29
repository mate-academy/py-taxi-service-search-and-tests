from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicTaxiTests(TestCase):
    def test_login_required_car_list(self) -> None:
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_list(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_list(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Homer",
            password="test1234",
            license_number="ABC12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="MX-5", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html",
        )

    def test_manufacturers_search(self) -> None:
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        form_data = {"name": "BMW"}
        response = self.client.get(MANUFACTURER_LIST_URL, data=form_data)
        queryset = Manufacturer.objects.filter(name__icontains="BMW")

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(queryset)
        )

    def test_retrieve_cars(self) -> None:
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="x5m", manufacturer=bmw
        )
        cars = Car.objects.all()
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html",
        )

    def test_cars_search(self) -> None:
        car = Car.objects.create(
            model="Mazda 6", manufacturer=self.manufacturer
        )
        car.drivers.add(self.user)
        form_data = {"model": "6"}
        response = self.client.get(CAR_LIST_URL, data=form_data)
        queryset = Car.objects.filter(model__icontains="6")

        self.assertEqual(
            list(response.context["car_list"]), list(queryset)
        )

    def test_retrieve_drivers(self) -> None:
        get_user_model().objects.create_user(
            username="Bart",
            password="test1234",
            license_number="XYZ98765"
        )
        drivers = Driver.objects.all()
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html",
        )

    def test_drivers_search(self) -> None:
        get_user_model().objects.create_user(
            username="Bart",
            password="test1234",
            license_number="XYZ98765"
        )
        form_data = {"username": "art"}
        response = self.client.get(DRIVER_LIST_URL, data=form_data)
        queryset = Driver.objects.filter(username__icontains="art")

        self.assertEqual(
            list(response.context["driver_list"]), list(queryset)
        )
