from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test", country="test country")
        Manufacturer.objects.create(name="test2", country="test country2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )

    def test_search_manufacturer(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")
        response = self.client.get(MANUFACTURER_URL, {"name": "Toyota"})
        manufacturers = response.context["manufacturer_list"]
        expected = Manufacturer.objects.filter(name__icontains="Toyota")
        self.assertEqual(list(manufacturers), list(expected))


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_date = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        self.client.post(
            reverse("taxi:driver-create"),
            data=form_date
        )
        new_user = get_user_model().objects.get(username=form_date["username"])

        self.assertEqual(new_user.first_name, form_date["first_name"])
        self.assertEqual(new_user.last_name, form_date["last_name"])
        self.assertEqual(new_user.license_number, form_date["license_number"])

    def test_retrieve_drivers(self):
        get_user_model().objects.create(
            username="test1234",
            password="test123",
            license_number="ABC12345"
        )
        get_user_model().objects.create(
            username="test2",
            password="test1234",
            license_number="AFD12345"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )

    def test_search_driver(self):
        get_user_model().objects.create(
            username="Ivan",
            password="Ivan123",
            license_number="ABC12345"
        )
        get_user_model().objects.create(
            username="Oleg",
            password="Oleg123",
            license_number="ABD12345"
        )
        get_user_model().objects.create(
            username="Luke",
            password="Luke123",
            license_number="ABF12345"
        )
        response = self.client.get(DRIVER_URL, {"driver": "Ivan"})
        drivers = response.context["driver_list"]
        expected = get_user_model().objects.filter(username__icontains="Ivan")
        self.assertEqual(list(drivers), list(expected))


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="pass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_create_car(self):
        form_date = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        self.client.post(
            reverse("taxi:car-create"),
            data=form_date
        )
        new_car = Car.objects.get(model=form_date["model"])

        self.assertEqual(new_car.model, form_date["model"])
        self.assertEqual(new_car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, new_car.drivers.all())

    def test_retrieve_cars(self):
        Car.objects.create(model="test", manufacturer=self.manufacturer)
        Car.objects.create(model="test2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )

    def test_search_car(self):
        Car.objects.create(model="test", manufacturer=self.manufacturer)
        Car.objects.create(model="test2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL, {"model": "test"})
        cars = response.context["car_list"]
        expected = Car.objects.filter(model__icontains="test")
        self.assertEqual(list(cars), list(expected))
