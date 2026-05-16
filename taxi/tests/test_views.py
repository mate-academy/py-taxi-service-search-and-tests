from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTests(TestCase):
    def test_login_required_manufacturer(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Volvo")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Volvo")
        response = self.client.get(MANUFACTURER_URL, {"name": "Volvo"})
        self.assertContains(response, "Volvo")
        self.assertNotContains(response, "BMW")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            first_name="test first",
            last_name="test last",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(name="BMW")

    def test_retrieve_car(self):
        car1 = Car.objects.create(
            model="X6",
            manufacturer=self.manufacturer
        )
        car1.drivers.add(self.driver)
        car2 = Car.objects.create(
            model="XC60",
            manufacturer=Manufacturer.objects.create(name="Volvo")
        )
        car2.drivers.add(self.driver)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_toggle_assign_to_car(self):
        car = Car.objects.create(model="Test", manufacturer=self.manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.id])
        self.client.post(url)
        self.assertTrue(car.drivers.filter(id=self.driver.id).exists())
        self.client.post(url)
        self.assertFalse(car.drivers.filter(id=self.driver.id).exists())

    def test_search_car(self):
        Car.objects.create(model="X3", manufacturer=self.manufacturer)
        Car.objects.create(model="X5", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL, {"model": "X5"})
        self.assertContains(response, "X5")
        self.assertNotContains(response, "X3")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            first_name="test first",
            last_name="test last",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABZ12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, "Test first")
        self.assertEqual(new_driver.last_name, "Test last")

    def test_search_driver(self):
        get_user_model().objects.create_user(
            username="Bob",
            password="test123",
            license_number="ABC12347",
        )
        get_user_model().objects.create_user(
            username="user",
            password="test123",
            license_number="ABC12346",
        )
        response = self.client.get(DRIVER_URL, {"username": "user"})
        self.assertContains(response, "user")
        self.assertNotContains(response, "Bob")
