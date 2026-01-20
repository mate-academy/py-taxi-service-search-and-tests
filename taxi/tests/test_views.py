from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from taxi.models import Car, Manufacturer, Driver


CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicPagesTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePagesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            license_number="TES99999"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Manufacturer_1", country="Country_1")
        Manufacturer.objects.create(name="Manufacturer_2", country="Country_2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "Manufacturer_1",
            "country": "Country_1",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="Driver_1",
            password="Password_1",
            first_name="First_1",
            last_name="Last_1",
            license_number="ABC12345",
        )
        Driver.objects.create(
            username="Driver_2",
            password="Password_2",
            first_name="First_2",
            last_name="Last_2",
            license_number="DEF67890",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "Driver_1",
            "password1": "test_Password",
            "password2": "test_Password",
            "first_name": "First_1",
            "last_name": "Last_1",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        driver = Driver.objects.get(username=form_data["username"])
        self.assertEqual(driver.username, form_data["username"])
        self.assertEqual(driver.first_name, form_data["first_name"])
        self.assertEqual(driver.last_name, form_data["last_name"])
        self.assertEqual(driver.license_number, form_data["license_number"])
