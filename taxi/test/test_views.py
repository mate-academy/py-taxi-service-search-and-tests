from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_REDIRECT_PUBLIC_URL = reverse("login")


class PrivateManufacturerListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="parker1",
            password="spider123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Lincoln", country="USA")
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Lincoln", country="USA")

        search_manufacturer = Manufacturer.objects.filter(name="lincoln")
        manufacturers = Manufacturer.objects.all()


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response, 200)
        self.assertTrue(response.url.startswith(DRIVER_REDIRECT_PUBLIC_URL))


class PrivateCarListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="forest",
            password="gump123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        Car.objects.create(model="test", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))

    def test_cars_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Bugatti",
            country="Italy"
        )
        Car.objects.create(model="Veyron", manufacturer=manufacturer)
        response = self.client.get("taxi:car-list")
        cars_search = Car.objects.filter(model="Bugatti S")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(cars_search))


class PublicDriverListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Andy",
            password="Andy123456",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        form_driver = {
            "username": "Woo12345",
            "password1": "Woo12345",
            "password2": "Woo12345",
            "license_number": "WOO12345",
            "first_name": "Woody",
            "last_name": "Allen"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_driver)
        response = self.client.get(DRIVER_LIST_URL)
        new_user = get_user_model().objects.get(username=form_driver["username"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_user.last_name, "Allen")
        self.assertEqual(new_user.first_name, form_driver["first_name"])
        self.assertTemplateUsed(response, "taxi:driver-list")

    def test_driver_search(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "test3"})
        driver_search = get_user_model().objects.filter(username="test3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(driver_search))