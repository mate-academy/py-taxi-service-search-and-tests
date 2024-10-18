from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


# Manufacturer update and delete URLS
def get_manufacturer_update_url(manufacturer: Manufacturer):
    return reverse("taxi:manufacturer-update", kwargs={"pk": manufacturer.pk})


def get_manufacturer_delete_url(manufacturer: Manufacturer):
    return reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.pk})


# Car update, delete and detail URLS
def get_car_update_url(car: Car):
    return reverse("taxi:car-update", kwargs={"pk": car.pk})


def get_car_delete_url(car: Car):
    return reverse("taxi:car-delete", kwargs={"pk": car.pk})


def get_car_detail_url(car: Car):
    return reverse("taxi:car-detail", kwargs={"pk": car.pk})


# Driver update, delete and detail URLS
def get_driver_update_url(driver: Driver):
    return reverse("taxi:driver-update", kwargs={"pk": driver.pk})


def get_driver_delete_url(driver: Driver):
    return reverse("taxi:driver-delete", kwargs={"pk": driver.pk})


def get_driver_detail_url(driver: Driver):
    return reverse("taxi:driver-detail", kwargs={"pk": driver.pk})


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )

    def test_login_required(self) -> None:
        for url in (
                MANUFACTURER_LIST_URL,
                MANUFACTURER_CREATE_URL,
                get_manufacturer_update_url(self.manufacturer),
                get_manufacturer_delete_url(self.manufacturer)
        ):
            http_response = self.client.get(url)
            self.assertNotEqual(
                http_response.status_code,
                200
            )


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test username",
            password="test_password123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Test Country"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="BMW",
            country="Test Country2"
        )
        self.all_manufacturers = Manufacturer.objects.all()
        self.manufacturer_data = {
            "name": "Updated Name",
            "country": "Updated Country"}
        self.client.force_login(self.user)

    def test_logged_in_user_access(self) -> None:
        for url in (
                MANUFACTURER_LIST_URL,
                MANUFACTURER_CREATE_URL,
                get_manufacturer_update_url(self.manufacturer),
                get_manufacturer_delete_url(self.manufacturer)
        ):
            http_response = self.client.get(url)
            self.assertEqual(
                http_response.status_code,
                200
            )

    def test_list(self) -> None:
        http_response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(
            list(http_response.context["manufacturer_list"]),
            list(self.all_manufacturers)
        )

    def test_list_search(self) -> None:
        for search_letter in ("a", "b", "s"):
            http_response = self.client.get(
                MANUFACTURER_LIST_URL,
                {"name": f"{search_letter}"}
            )
            self.assertEqual(
                list(http_response.context["manufacturer_list"]),
                list(self.all_manufacturers.filter(
                    name__icontains=f"{search_letter}")
                )
            )

    def test_create(self) -> None:
        http_response = self.client.post(
            MANUFACTURER_CREATE_URL,
            data=self.manufacturer_data
        )
        manufacturer = Manufacturer.objects.get(
            name=self.manufacturer_data["name"]
        )

        self.assertEqual(
            manufacturer.country,
            self.manufacturer_data["country"]
        )
        self.assertEqual(
            http_response.status_code,
            302
        )

    def test_update(self) -> None:
        http_response = self.client.post(
            get_manufacturer_update_url(self.manufacturer),
            data=self.manufacturer_data
        )
        manufacturer = Manufacturer.objects.get(
            name=self.manufacturer_data["name"]
        )

        self.assertEqual(
            manufacturer.country,
            self.manufacturer_data["country"]
        )
        self.assertEqual(
            http_response.status_code,
            302
        )

    def test_delete(self) -> None:
        self.client.post(get_manufacturer_delete_url(self.manufacturer))
        self.client.post(get_manufacturer_delete_url(self.manufacturer_2))
        self.assertFalse(len(self.all_manufacturers))


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )

    def test_login_required(self) -> None:
        for url in (
                CAR_LIST_URL,
                CAR_CREATE_URL,
                get_car_update_url(self.car),
                get_car_delete_url(self.car),
                get_car_detail_url(self.car),
        ):
            http_response = self.client.get(url)
            self.assertNotEqual(
                http_response.status_code,
                200
            )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2"
        )
        self.car = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer,
        )
        self.car_2 = Car.objects.create(
            model="M6",
            manufacturer=self.manufacturer
        )
        self.car_data = {
            "model": "New Model",
            "manufacturer": self.manufacturer_2.id,
            "drivers": []
        }

        self.all_cars = Car.objects.all()
        self.client.force_login(self.user)

    def test_logged_in_user_access(self) -> None:
        for url in (
                CAR_LIST_URL,
                CAR_CREATE_URL,
                get_car_detail_url(self.car),
                get_car_update_url(self.car),
                get_car_delete_url(self.car)
        ):
            http_response = self.client.get(url)
            self.assertEqual(
                http_response.status_code,
                200
            )

    def test_list(self) -> None:
        http_response = self.client.get(CAR_LIST_URL)
        self.assertEqual(
            list(http_response.context["car_list"]),
            list(self.all_cars)
        )

    def test_list_search(self) -> None:
        for search_letter in ("5", "6", "m"):
            http_response = self.client.get(
                CAR_LIST_URL,
                {"model": f"{search_letter}"}
            )
            self.assertEqual(
                list(http_response.context["car_list"]),
                list(self.all_cars.filter(model__icontains=f"{search_letter}"))
            )

    def test_detail(self) -> None:
        self.assertEqual(
            self.client.get(get_car_detail_url(self.car)).context["car"],
            self.car
        )
        self.assertEqual(
            self.client.get(get_car_detail_url(self.car_2)).context["car"],
            self.car_2
        )

    def test_create(self) -> None:
        http_response = self.client.post(
            CAR_CREATE_URL,
            data=self.car_data
        )
        car = Car.objects.get(
            model=self.car_data["model"]
        )
        self.assertEqual(
            http_response.status_code,
            302
        )
        self.assertEqual(
            car.manufacturer,
            self.manufacturer_2
        )

    def test_update(self) -> None:
        http_response = self.client.post(
            get_car_update_url(self.car),
            data=self.car_data
        )
        car = Car.objects.get(
            model=self.car_data["model"]
        )
        self.assertEqual(
            http_response.status_code,
            302
        )
        self.assertEqual(
            car.manufacturer,
            self.manufacturer_2
        )

    def test_delete(self) -> None:
        http_response = self.client.post(get_car_delete_url(self.car))
        http_response_2 = self.client.post(get_car_delete_url(self.car_2))
        self.assertEqual(
            http_response.status_code,
            302
        )
        self.assertEqual(
            http_response_2.status_code,
            302
        )

        self.assertFalse(len(self.all_cars))


class DriverPublicTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Test Name",
            password="password_123"
        )

    def test_login_required(self) -> None:
        for url in (
                DRIVER_LIST_URL,
                DRIVER_CREATE_URL,
                get_driver_update_url(self.driver),
                get_driver_delete_url(self.driver),
                get_driver_detail_url(self.driver)
        ):
            http_response = self.client.get(url)
            self.assertNotEqual(
                http_response.status_code,
                200
            )


class DriverPrivateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user1",
            password="test_password123"
        )
        self.driver = get_user_model().objects.create_user(
            username="Test Name 2",
            password="password_123",
            license_number="ABC12345"
        )
        self.all_drivers = get_user_model().objects.all()
        self.driver_data = {
            "username": "NewDriver",
            "password1": "new_driver_password",
            "password2": "new_driver_password",
            "license_number": "BCD12346"
        }
        self.client.force_login(self.user)

    def test_logged_in_user_access(self) -> None:
        for url in (
                DRIVER_LIST_URL,
                DRIVER_CREATE_URL,
                get_driver_detail_url(self.driver),
                get_driver_update_url(self.driver),
                get_driver_delete_url(self.driver)
        ):
            http_response = self.client.get(url)
            self.assertEqual(
                http_response.status_code,
                200
            )

    def test_list(self) -> None:
        http_response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(
            list(http_response.context["driver_list"]),
            list(self.all_drivers)
        )

    def test_list_search(self) -> None:
        for search_letter in ("1", "2", "t"):
            http_response = self.client.get(
                DRIVER_LIST_URL,
                {"username": f"{search_letter}"}
            )
            self.assertEqual(
                list(http_response.context["driver_list"]),
                list(self.all_drivers.filter(
                    username__icontains=f"{search_letter}")
                )
            )

    def test_detail(self) -> None:
        self.assertEqual(
            self.client.get(
                get_driver_detail_url(self.user)).context["driver"],
            self.user
        )
        self.assertEqual(
            self.client.get(
                get_driver_detail_url(self.driver)).context["driver"],
            self.driver
        )

    def test_create(self) -> None:
        http_response = self.client.post(
            DRIVER_CREATE_URL,
            data=self.driver_data
        )
        new_driver = get_user_model().objects.get(
            username=self.driver_data["username"]
        )
        self.assertEqual(
            http_response.status_code,
            302
        )
        self.assertEqual(
            new_driver.license_number,
            self.driver_data["license_number"]
        )
        self.assertTrue(
            new_driver.check_password(self.driver_data["password1"])
        )

    def test_update(self) -> None:
        http_response = self.client.post(
            get_driver_update_url(self.driver),
            data={
                "license_number": self.driver_data["license_number"]
            }
        )
        new_driver = get_user_model().objects.get(
            username=self.driver.username
        )
        self.assertEqual(
            http_response.status_code,
            302
        )
        self.assertEqual(
            new_driver.license_number,
            self.driver_data["license_number"]
        )

    def test_delete(self) -> None:
        http_response = self.client.post(
            get_driver_delete_url(self.driver)
        )
        self.assertEqual(
            http_response.status_code,
            302
        )
        self.assertEqual(
            len(self.all_drivers),
            1
        )
