from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturer(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturer(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1234"
        )

        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Renault", country="France")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_URL + "?name=Ford")

        manufacturer = Manufacturer.objects.filter(
            name__icontains="Ford"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )


class PublicCar(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCar(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1234"
        )

        self.client.force_login(self.user)

        ford = Manufacturer.objects.create(name="Ford", country="USA")
        renault = Manufacturer.objects.create(name="Renault", country="France")

        Car.objects.create(model="Fiesta", manufacturer=ford)
        Car.objects.create(model="Logan", manufacturer=renault)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search(self):
        response = self.client.get(CAR_URL + "?model=Fiesta")

        car = Car.objects.filter(
            model__icontains="Fiesta"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car),
        )

    def test_car_detail_response_with_correct_template(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PublicDriver(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriver(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1234"
        )

        self.client.force_login(self.user)

        Driver.objects.create(username="driver_1", license_number="BOB09631")
        Driver.objects.create(username="driver_2", license_number="BIL39231")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search(self):
        response = self.client.get(DRIVER_URL + "?username=driver_1")

        driver = Driver.objects.filter(
            username__icontains="driver_1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver),
        )

    def test_driver_detail_response_with_correct_template(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
