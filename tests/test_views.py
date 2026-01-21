from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="bobius",
            password="123456te",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Test1", country="Test1")
        Manufacturer.objects.create(name="Test2", country="Test2")

        response = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        response = self.client.get("/manufacturers/?username=FC")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="FC")
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="bobius",
            password="123456te",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        first_manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Test1"
        )
        second_manufacturer = Manufacturer.objects.create(
            name="Test2",
            country="Test2"
        )
        Car.objects.create(model="Test1", manufacturer=first_manufacturer)
        Car.objects.create(model="Test2", manufacturer=second_manufacturer)

        response = self.client.get(CAR_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search(self):
        response = self.client.get("/cars/?username=YA")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="YA")
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="bobius",
            password="123456te",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="Test1",
            password="Test1",
            license_number="AAA12345"
        )
        get_user_model().objects.create_user(
            username="Test2",
            password="Test2",
            license_number="BBB12345"
        )

        response = self.client.get(DRIVER_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test1",
            "last_name": "Test2",
            "license_number": "AAA12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_search(self):
        response = self.client.get("/drivers/?username=A")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="A")
        )
