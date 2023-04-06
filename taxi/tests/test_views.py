from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_public_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Testusername", password="testpass123456"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Ford", country="United States")
        Manufacturer.objects.create(name="Tesla", country="United States")

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            manufacturer,
            ordered=False
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_URL + "?name=ford")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_after_searching_by_name(self):
        manufacturer_queryset = Manufacturer.objects.filter(
            name__icontains="f"
        )
        response = self.client.get(MANUFACTURER_URL + "?name=f")

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            manufacturer_queryset,
            transform=lambda x: x
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_public_car(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123456"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford", country="United States"
        )
        Car.objects.create(
            model="lotus",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="astra",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="patriot",
            manufacturer=self.manufacturer
        )

    def test_private_car(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search(self):
        cars_queryset = Car.objects.filter(model__icontains="lo")
        response = self.client.get(CAR_URL + "?model=lo")

        self.assertEqual(
            list(
                response.context["car_list"]
            ), list(cars_queryset)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_after_searching_by_model(self):
        car_queryset = Car.objects.filter(
            model__icontains="ast"
        )
        response = self.client.get(CAR_URL + "?model=ast")

        self.assertEqual(
            list(
                response.context["car_list"]
            ), list(car_queryset)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_public_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Testusername", password="testpass123456"
        )
        self.client.force_login(self.user)
        Driver.objects.create(
            username="antonylaros",
            password="testpass123456",
            license_number="KKK12345",
            first_name="firstname",
            last_name="lastname",
        )
        Driver.objects.create(
            username="markstoner",
            password="testpass123456",
            license_number="TTT12345",
            first_name="firstname1",
            last_name="lastname1",
        )
        Driver.objects.create(
            username="bobross",
            password="testpass123456",
            license_number="WWW12345",
            first_name="firstname2",
            last_name="lastname2",
        )

    def test_private_driver(self):
        response = self.client.get(DRIVER_URL)
        driver = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
        self.assertTemplateUsed(response.context)

    def test_driver_search(self):
        response = self.client.get(DRIVER_URL + "?username=mark")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_after_searching_by_username(self):
        driver_queryset = Driver.objects.filter(
            username__icontains="mark"
        )
        response = self.client.get(DRIVER_URL + "?username=mark")

        self.assertEqual(
            list(
                response.context["driver_list"]
            ), list(driver_queryset)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="bobross123", password="pass12345", license_number="HHH12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Yaris",
        )

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.id])
        )
        self.driver.refresh_from_db()
        if self.car in self.driver.cars.all():
            self.client.get(
                reverse("taxi:toggle-car-assign", args=[self.car.id])
            )
            self.assertNotIn(self.car, self.driver.cars.all())
        else:
            self.client.get(
                reverse("taxi:toggle-car-assign", args=[self.car.id])
            )
            self.assertIn(self.car, self.driver.cars.all())
