from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
MANUFACTURERS_URL_WITH_SEARCH = reverse("taxi:manufacturer-list") + "?name=F"
CARS_URL = reverse("taxi:car-list")
CARS_URL_WITH_SEARCH = reverse("taxi:car-list") + "?model=V"
DRIVERS_URL = reverse("taxi:driver-list")
DRIVERS_URL_WITH_SEARCH = reverse("taxi:driver-list") + "?username=1"


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Ferrari")

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_with_search(self):
        response = self.client.get(MANUFACTURERS_URL_WITH_SEARCH)

        manufacturers = Manufacturer.objects.filter(name__icontains="F")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Honda")
        Car.objects.create(
            model="Honda Accord",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Honda HR-V",
            manufacturer=manufacturer
        )

    def test_retrieve_car(self):
        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_with_search(self):
        response = self.client.get(CARS_URL_WITH_SEARCH)

        cars = Car.objects.filter(model__icontains="V")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(self.admin_user)
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="driver23451",
            license_number="DRV12345",
        )

    def test_retrieve_driver(self):
        response = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_with_search(self):
        response = self.client.get(DRIVERS_URL_WITH_SEARCH)

        drivers = Driver.objects.filter(username__icontains="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test_First",
            "last_name": "Test_Last",
            "license_number": "TST12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
