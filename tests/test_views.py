from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1111",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test_name1", country="test_country1")
        Manufacturer.objects.create(name="test_name2", country="test_country2")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        response = self.client.get(MANUFACTURERS_URL, {"name": "test_name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name="test_name"))
        )


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1111",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car1 = Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )
        car2 = Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )
        car1.drivers.add(self.user)
        car2.drivers.add(self.user)
        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )
        Car.objects.create(model="test_model", manufacturer=manufacturer)
        Car.objects.create(model="new_model", manufacturer=manufacturer2)
        response = self.client.get(CARS_URL, {"model": "test_model"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model="test_model"))
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1111",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "testpassword1234",
            "password2": "testpassword1234",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(user.first_name, form_data["first_name"])
        self.assertEqual(user.last_name, form_data["last_name"])
        self.assertEqual(user.license_number, form_data["license_number"])

    def test_driver_search(self):
        Driver.objects.create(
            username="test_driver1",
            password="passowrd12345",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="test_driver2",
            password="passowrd12342",
            license_number="ABC12342"
        )
        response = self.client.get(DRIVERS_URL, {"username": "driver"})
        drivers = Driver.objects.filter(username__icontains="driver")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
