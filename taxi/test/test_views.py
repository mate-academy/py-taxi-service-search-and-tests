from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class ModuleListViewSearchTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="<PASSWORD123>",
            license_number="ASD54321",
        )
        self.driver_one = Driver.objects.create(
            username="testdriver", license_number="ASD54381")
        self.driver_two = Driver.objects.create(
            username="driver_two", license_number="ASD54391")
        self.driver_three = Driver.objects.create(
            username="another_driver", license_number="ASD54101")
        self.manufacturer_one = Manufacturer.objects.create(
            name="manufacturertest", country="USC")
        self.manufacturer_two = Manufacturer.objects.create(
            name="two_manufacturer", country="USP")
        self.manufacturer_three = Manufacturer.objects.create(
            name="manufacturer_another", country="USB")
        self.car_one = Car(
            model="Toyota", manufacturer=self.manufacturer_one, id=1)
        self.car_two = Car(
            model="Another_Toyota", manufacturer=self.manufacturer_two, id=2)
        self.car_three = Car(
            model="testToyota", manufacturer=self.manufacturer_three, id=3)
        self.car_one.drivers.add(self.driver_one)
        self.car_one.drivers.add(self.driver_two)
        self.car_one.save()
        self.car_two.drivers.add(self.driver_one)
        self.car_two.drivers.add(self.driver_three)
        self.car_two.save()
        self.car_three.drivers.add(self.driver_three)
        self.car_three.drivers.add(self.driver_two)
        self.car_three.save()

    def test_search_cars_group_correct_model(self):
        self.client.login(username="driver", password="<PASSWORD123>")
        response = self.client.get(CAR_LIST_URL, {"model": "toyota"})
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Another_Toyota")
        self.assertContains(response, "testToyota")
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_search_car_correct_model(self):
        self.client.login(username="driver", password="<PASSWORD123>")
        response = self.client.get(CAR_LIST_URL, {"model": "another"})
        self.assertContains(response, "Another_Toyota")
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_search_manufacturer_correct_name(self):
        self.client.login(username="driver", password="<PASSWORD123>")
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "test"})
        self.assertContains(response, self.manufacturer_one.name)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_search_manufacturers_group_correct_name(self):
        self.client.login(username="driver", password="<PASSWORD123>")
        response = (self.client.
                    get(MANUFACTURER_LIST_URL, {"name": "manufacturer"}))
        self.assertContains(response, self.manufacturer_one.name)
        self.assertContains(response, self.manufacturer_two.name)
        self.assertContains(response, self.manufacturer_three.name)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_driver_correct_username(self):
        self.client.login(username="driver", password="<PASSWORD123>")
        response = self.client.get(DRIVER_LIST_URL, {"username": "testdriver"})
        self.assertContains(response, self.driver_one.username)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_search_drivers_group_correct_username(self):
        self.client.login(username="driver", password="<PASSWORD123>")
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver"})
        self.assertContains(response, self.driver_one.username)
        self.assertContains(response, self.driver_two.username)
        self.assertContains(response, self.driver_three.username)
        self.assertContains(response, self.driver.username)
        self.assertEqual(len(response.context["driver_list"]), 4)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_private_cars(self):
        driver_one = get_user_model().objects.create(
            license_number="ASD12345",
            username="test1",
            first_name="John1",
            last_name="Doe1",
        )
        driver_two = get_user_model().objects.create(
            license_number="ASD54321",
            username="test2",
            first_name="John2",
            last_name="Doe2",
        )
        manufacturer = Manufacturer.objects.create(name="test", country="US")
        car = Car(model="test", manufacturer=manufacturer, id=1)
        car.drivers.add(driver_one)
        car.drivers.add(driver_two)
        car.save()
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars),
        )

    def test_private_driver(self):
        Driver.objects.create(
            license_number="ASD12345",
            username="user2",
        )
        Driver.objects.create(
            license_number="ASD54321",
            username="user1",
        )
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers),
        )

    def test_private_manufacturers(self):
        Manufacturer.objects.create(name="test", country="US")
        Manufacturer.objects.create(name="test123", country="US123")
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
