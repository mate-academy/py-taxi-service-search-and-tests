from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class ManufacturerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        driver = get_user_model().objects.create(
            username="test_username",
            password="test_password",
            license_number="TST12345"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        car.drivers.add(driver)

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)


class PublicTest(TestCase):
    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Manufacturer.objects.create(
            name="test_name_2",
            country="test_country_2"
        )
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test_model_2",
            manufacturer=manufacturer
        )
        cars = Car.objects.all()
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self) -> None:
        get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            license_number="AAA12345",
        )
        get_user_model().objects.create_user(
            username="test_username_2",
            password="test_password_2",
            license_number="BBB12345",
        )
        drivers = Driver.objects.all()
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class AdminPanelTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_username",
            password="admin_password"
        )
        self.client.force_login(self.admin_user)

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            driver.get_absolute_url(), "/drivers/1/"
        )
