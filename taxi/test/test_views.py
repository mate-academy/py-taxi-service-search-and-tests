import itertools
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")

manufacturer_counter = itertools.count(1)

def sample_manufacturer(name=None, country="Germany"):
    if not name:
        name = f"Manufacturer{next(manufacturer_counter)}"
    return Manufacturer.objects.create(name=name, country=country)


def sample_car(model="Civic", manufacturer=None):
    if not manufacturer:
        manufacturer = sample_manufacturer()
    return Car.objects.create(model=model, manufacturer=manufacturer)


def sample_driver(username="driver1", password="testpass123", license_number="ABC12345"):
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        license_number=license_number,
    )


class PublicAccessTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_manufacturer_list_requires_login(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_list_requires_login(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_requires_login(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        m1 = sample_manufacturer(name="BMW")
        m2 = sample_manufacturer(name="Fiat", country="Italy")

        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "BMW"})

        self.assertContains(res, m1.name)
        self.assertNotContains(res, m2.name)


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        c1 = sample_car(model="Continental")
        c2 = sample_car(model="Civic")

        res = self.client.get(CAR_LIST_URL, {"model": "Continental"})

        self.assertContains(res, c1.model)
        self.assertNotContains(res, c2.model)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        d1 = sample_driver(username="john_doe", license_number="12345")
        d2 = sample_driver(username="jane_doe", license_number="67890")

        res = self.client.get(DRIVER_LIST_URL, {"username": "john"})

        self.assertContains(res, d1.username)
        self.assertNotContains(res, d2.username)


class CarDetailViewTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)

    def test_car_detail_displays_manufacturer_and_drivers(self):
        manufacturer = sample_manufacturer(name="Audi")
        car = sample_car(model="Q7", manufacturer=manufacturer)
        car.drivers.add(self.user)

        url = reverse("taxi:car-detail", args=[car.id])
        res = self.client.get(url)

        self.assertContains(res, car.model)
        self.assertContains(res, car.manufacturer.name)
        self.assertContains(res, self.user.username)


class DriverDetailViewTests(TestCase):
    def setUp(self):
        self.user = sample_driver(username="alex", license_number="AAA111")
        self.client.force_login(self.user)

    def test_driver_detail_displays_cars_and_manufacturers(self):
        car1 = sample_car(model="X5")
        car2 = sample_car(model="Q7")
        self.user.cars.add(car1, car2)

        url = reverse("taxi:driver-detail", args=[self.user.id])
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, car1.model)
        self.assertContains(res, car1.manufacturer.name)
        self.assertContains(res, car2.model)


class ManufacturerFormTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        url = reverse("taxi:manufacturer-create")
        data = {"name": "Tesla", "country": "USA"}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Tesla").exists())

    def test_update_manufacturer(self):
        manufacturer = sample_manufacturer(name="Audi", country="Germany")
        url = reverse("taxi:manufacturer-update", args=[manufacturer.id])
        data = {"name": "Audi Updated", "country": "Germany"}
        res = self.client.post(url, data)

        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "Audi Updated")

    def test_delete_manufacturer(self):
        manufacturer = sample_manufacturer()
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(id=manufacturer.id).exists())


class CarFormTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)
        self.manufacturer = sample_manufacturer(name="Mercedes")

    def test_create_car(self):
        url = reverse("taxi:car-create")
        data = {
            "model": "E-Class",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Car.objects.filter(model="E-Class").exists())

    def test_update_car(self):
        car = sample_car(model="C-Class", manufacturer=self.manufacturer)
        car.drivers.add(self.user)
        url = reverse("taxi:car-update", args=[car.id])
        data = {"model": "C-Class Updated",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],}
        res = self.client.post(url, data)

        car.refresh_from_db()
        self.assertEqual(car.model, "C-Class Updated")

    def test_delete_car(self):
        car = sample_car(model="GLA", manufacturer=self.manufacturer)
        url = reverse("taxi:car-delete", args=[car.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class DriverFormTests(TestCase):
    def setUp(self):
        self.user = sample_driver()
        self.client.force_login(self.user)

    def test_create_driver(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "new_driver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "NEW12345",
        }

        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="new_driver").exists())



    def test_delete_driver(self):
        driver = self.user
        url = reverse("taxi:driver-delete", args=[driver.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Driver.objects.filter(id=driver.id).exists())