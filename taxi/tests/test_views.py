from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEquals(res.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturers(self):
        query_params = {"name": "B"}
        search_url = MANUFACTURER_URL + "?" + urlencode(query_params)
        response = self.client.get(search_url)

        self.assertEqual(response.status_code, 200)

        manufacturer_list = response.context_data["manufacturer_list"]
        filtered_manufacturers_b = Manufacturer.objects.filter(
            name__icontains="B"
        )
        self.assertEqual(
            list(manufacturer_list),
            list(filtered_manufacturers_b)
        )

        query_params = {"name": "M"}
        search_url = MANUFACTURER_URL + "?" + urlencode(query_params)
        response = self.client.get(search_url)

        manufacturer_list = response.context_data["manufacturer_list"]
        filtered_manufacturers_m = Manufacturer.objects.filter(
            name__icontains="M"
        )
        self.assertEqual(
            list(manufacturer_list),
            list(filtered_manufacturers_m)
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )
        Car.objects.create(model="test", manufacturer=self.manufacturer1)
        Car.objects.create(model="test1", manufacturer=self.manufacturer2)

    def test_retrieve_cars(self):
        res = self.client.get(CAR_URL)
        self.assertEquals(res.status_code, 200)
        car = Car.objects.all()
        self.assertEquals(list(res.context["car_list"]), list(car))

    def test_car_search(self):
        query_params = {"model": "test"}
        search_url = CAR_URL + "?" + urlencode(query_params)
        response = self.client.get(search_url)

        self.assertEqual(response.status_code, 200)

        car_list = response.context_data["car_list"]
        filtered_cars = Car.objects.filter(model__icontains="test")
        self.assertEqual(list(car_list), list(filtered_cars))

        query_params = {"model": "1"}
        search_url = CAR_URL + "?" + urlencode(query_params)
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, 200)
        car_list = response.context_data["car_list"]
        filtered_cars = Car.objects.filter(model__icontains="1")
        self.assertEqual(list(car_list), list(filtered_cars))


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Driver.objects.create(
            username="test_driver1",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="test_driver2",
            license_number="ADC12345"
        )

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_URL)
        self.assertEquals(res.status_code, 200)

    def test_driver_search(self):
        query_params = {"username": "test"}
        search_url = DRIVER_URL + "?" + urlencode(query_params)
        response = self.client.get(search_url)

        self.assertEqual(response.status_code, 200)

        driver_list = response.context_data["driver_list"]
        filtered_drivers = Driver.objects.filter(username__icontains="test")
        self.assertEqual(list(driver_list), list(filtered_drivers))

        query_params = {"username": "driver"}
        search_url = DRIVER_URL + "?" + urlencode(query_params)
        response = self.client.get(search_url)

        self.assertEqual(response.status_code, 200)

        driver_list = response.context_data["driver_list"]
        filtered_drivers = Driver.objects.filter(username__icontains="driver")
        self.assertEqual(list(driver_list), list(filtered_drivers))
