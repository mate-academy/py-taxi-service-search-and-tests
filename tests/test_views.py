from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
MANUFACTURERS_SEARCH_URL = reverse("taxi:manufacturer-list") + "?name=a"
DRIVERS_URL = reverse("taxi:driver-list")
DRIVERS_SEARCH_URL = reverse("taxi:driver-list") + "?username=a"
CAR_URL = reverse("taxi:car-list")
CAR_SEARCH_URL = reverse("taxi:car-list") + "?model=a"


class PublicPagesTest(TestCase):
    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturers_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_drivers_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_cars_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="lkjhfdsa",
            first_name="Driver",
            last_name="Driverio",
            license_number="OIU29032"
        )
        self.client.force_login(self.driver)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Miwa", country="Test")
        Manufacturer.objects.create(name="Vovchoik", country="Test")
        Manufacturer.objects.create(name="Vasilivich", country="Test")
        res = self.client.get(MANUFACTURERS_SEARCH_URL)
        manufacturers = Manufacturer.objects.filter(name__icontains="a")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="lkjhfdsa",
            first_name="Driver",
            last_name="Driverio",
            license_number="OIU29032"
        )
        self.client.force_login(self.driver)

    def test_search_manufacturer_by_name(self):
        get_user_model().objects.create(
            username="user_1a",
            password="password",
            license_number="MVO45256"
        )
        get_user_model().objects.create(
            username="user_1b",
            password="password",
            license_number="VOM45879"
        )
        get_user_model().objects.create(
            username="user_1c",
            password="password",
            license_number="VOM79663"
        )
        res = self.client.get(DRIVERS_SEARCH_URL)
        drivers = Driver.objects.filter(username__icontains="a")
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="1qazcde3r",
            first_name="Driver",
            last_name="Driver_miwa",
            license_number="MVO45888"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Volvo",
            country="Sweden"
        )
        self.client.force_login(self.driver)

    def test_car_search_by_model(self):
        Car.objects.create(model="BMX", manufacturer=self.manufacturer)
        Car.objects.create(model="Volvo", manufacturer=self.manufacturer)
        cars = list(Car.objects.filter(
            model__icontains="a"
        ))
        res = self.client.get(CAR_SEARCH_URL)

        self.assertEqual(
            list(res.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_toggle_assign_to_car(self):

        car = Car.objects.create(
            model="Model-X",
            manufacturer=self.manufacturer
        )

        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(car in self.driver.cars.all())

        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(car in self.driver.cars.all())
