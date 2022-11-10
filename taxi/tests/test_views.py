from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.views import ManufacturerListView


class PublicAllViewsTests(TestCase):
    def test_login_required_manufacturer(self) -> None:
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self) -> None:
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver(self) -> None:
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="sandychicks",
            license_number="JKQ12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Honda", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Mercedes", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(len(response.context['manufacturer_list']), ManufacturerListView.paginate_by)


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="sandychicks",
            license_number="JKQ12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="Honda", country="Japan")
        Car.objects.create(model="Civic", manufacturer=manufacturer)
        Car.objects.create(model="Accord", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class DriverCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="sandychicks",
            password="123chicks",
            license_number="JKQ12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        get_user_model().objects.create_user(
            username="patrik",
            password="123patrick",
            license_number="ABC54213",
        )
        get_user_model().objects.create_user(
            username="spongebob",
            password="098sponge",
            license_number="BNA83940",
        )

        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


