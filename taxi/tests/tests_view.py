from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

INDEX_URL = reverse("taxi:index")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicIndexViewTests(TestCase):
    def test_index_access(self) -> None:
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicDriverListViewTests(TestCase):
    def test_driver_list_access(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarListViewTests(TestCase):
    def test_car_list_access(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerListViewTests(TestCase):
    def test_manufacturer_list_access(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver", password="password"
        )
        self.client.force_login(self.user)

        Driver.objects.create(username="user1", license_number="ABC12345")
        Driver.objects.create(username="user2", license_number="ABC54321")

    def test_retrieve_driver_list(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username(self) -> None:
        response = self.client.get(DRIVER_LIST_URL, {"username": "user1"})
        drivers = Driver.objects.filter(username__icontains="user1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver", password="password"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )
        Car.objects.create(model="Car1", manufacturer=self.manufacturer)
        Car.objects.create(model="Car2", manufacturer=self.manufacturer)

    def test_retrieve_car_list(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_by_model(self) -> None:
        response = self.client.get(CAR_LIST_URL, {"model": "Car1"})
        cars = Car.objects.filter(model__icontains="Car1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateManufacturerListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver", password="password"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Manufacturer1", country="Country1")
        Manufacturer.objects.create(name="Manufacturer2", country="Country2")

    def test_retrieve_manufacturer_list(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self) -> None:
        response = self.client.get(
            MANUFACTURER_LIST_URL, {"name": "Manufacturer1"}
        )
        manufacturers = Manufacturer.objects.filter(
            name__icontains="Manufacturer1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
