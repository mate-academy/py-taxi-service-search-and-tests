from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


from taxi.models import Manufacturer, Car, Driver


MANUFACTURES_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURES_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test1234")

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Mercedes", country="Germany")

        manufacturers = Manufacturer.objects.all()

        response = self.client.get(MANUFACTURES_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_option(self):
        url = MANUFACTURES_URL + "?=username=est"
        response = self.client.get(url)
        self.assertQuerysetEqual(
            Manufacturer.objects.filter(
                name__icontains="est"),
            response.context["manufacturer_list"])


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test1234")

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="Test_case_1",
            password="test1234",
            license_number="DHF12345")
        get_user_model().objects.create_user(
            username="Test_case_2",
            password="test4321",
            license_number="DHF54321")

        drivers = get_user_model().objects.all()

        response = self.client.get(DRIVERS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search_option(self):
        url = DRIVERS_URL + "?=username=est"
        response = self.client.get(url)
        self.assertQuerysetEqual(
            Driver.objects.filter(username__icontains="est"),
            response.context["driver_list"])


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test1234")

        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="TestName",
                                                   country="TestCountry")

        Car.objects.create(model="Test",
                                 manufacturer=manufacturer)
        cars = Car.objects.all()

        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search_option(self):
        url = CAR_URL + "?=model=es"
        response = self.client.get(url)
        self.assertQuerysetEqual(Car.objects.filter(
            model__icontains="es"),
            response.context["car_list"])
