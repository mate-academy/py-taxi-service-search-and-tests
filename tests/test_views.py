from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PrivateTestBase(TestCase):
    def setUp(self):
        username = "Driver"
        password = "driver456"
        license_number = "MOP23456"
        first_name = "test_first"
        last_name = "test_last"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name
        )
        self.client.force_login(self.user)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(PrivateTestBase):
    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test_Manufacturer",
            country="Test_Country"
        )
        Manufacturer.objects.create(
            name="Test_Manufacturer_1",
            country="Test_Country_1"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers_by_name(self):
        Manufacturer.objects.create(
            name="First_Manufacturer",
            country="Test_Country1"
        )
        Manufacturer.objects.create(
            name="Second_Manufacturer",
            country="Test_Country2"
        )
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": "First_Manufacturer"}
        )
        self.assertContains(response, "First_Manufacturer")
        self.assertNotContains(response, "Second_Manufacturer")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(PrivateTestBase):
    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_Manufacturer",
            country="Test_Country"
        )
        Car.objects.create(model="Test_Car1", manufacturer=manufacturer)
        Car.objects.create(model="Test_Car2", manufacturer=manufacturer)

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_manufacturers_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="First_Manufacturer",
            country="Test_Country1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Second_Manufacturer",
            country="Test_Country2"
        )
        Car.objects.create(model="Test_Car1", manufacturer=manufacturer1)
        Car.objects.create(model="Test_Car2", manufacturer=manufacturer2)
        response = self.client.get(CAR_URL, {"model": "Test_Car1"})
        self.assertContains(response, "Test_Car1")
        self.assertNotContains(response, "Test_Car2")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(PrivateTestBase):
    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_detail_driver(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.user.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        form_data = {
            "username": "Driver",
            "password": "driver456",
            "license_number": "MOP23456",
            "first_name": "test_first",
            "last_name": "test_last",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_update_driver(self):
        new_license_number = "MOP23456"
        self.client.post(reverse("taxi:driver-update", args=[self.user.id]),
                         data={"license_number": new_license_number})
        self.assertEqual(new_license_number, self.user.license_number)

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="driver123",
            license_number="POL39485",
            password="<PASSWORD>"
        )
        self.client.post(reverse("taxi:driver-delete", args=[driver.id]))
        self.assertFalse(get_user_model().objects.filter(
            username="driver123"
        ).exists())

    def test_search_drivers_by_username(self):
        get_user_model().objects.create_user(
            username="driver123",
            license_number="POL39455",
            password="<PASSWORD1>"
        )
        get_user_model().objects.create_user(
            username="driver421",
            license_number="POL39485",
            password="<PASSWORD2>"
        )
        response = self.client.get(DRIVER_URL, {"username": "driver123"})
        self.assertContains(response, "driver123")
        self.assertNotContains(response, "driver421")
