from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.views import toggle_assign_to_car

URLS = {
    "HOME_URL": reverse("taxi:index"),
    "MANUFACTURER_LIST_PAGE_URL": reverse("taxi:manufacturer-list"),
    "CAR_LIST_PAGE_URL": reverse("taxi:car-list"),
    "DRIVER_LIST_PAGE_URL": reverse("taxi:driver-list"),

}


class PublicModelsTest(TestCase):
    def test_login_required(self):
        for url in URLS.values():
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateModelsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "user1",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="NI-SAN", country="Japan")

        res = self.client.get(URLS["MANUFACTURER_LIST_PAGE_URL"])
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )

    def test_retrieve_cars(self):
        manufacturer1 = Manufacturer.objects.create(name="Tesla", country="USA")
        manufacturer2 = Manufacturer.objects.create(name="NI-SAN", country="Japan")
        Car.objects.create(model="BMW", manufacturer=manufacturer1)
        Car.objects.create(model="NI-SAN", manufacturer=manufacturer2)

        res = self.client.get(URLS["CAR_LIST_PAGE_URL"])
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )

    def test_retrieve_drivers(self):
        Driver.objects.create_user(username="west",
                                   password="user1",
                                   first_name="John",
                                   last_name="Brown",
                                   license_number="FER3124")

        Driver.objects.create_user(username="north",
                                   password="user2",
                                   first_name="Andrew",
                                   last_name="Brown",
                                   license_number="CDF53479")

        res = self.client.get(URLS["DRIVER_LIST_PAGE_URL"])
        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )

    def test_create_driver_through_form(self):
        data = {
            "username": "admin321",
            "password1": "grtyh12345",
            "password2": "grtyh12345",
            "first_name": "Andrew",
            "last_name": "Brown",
            "license_number": "QWE98726"
        }
        self.client.post(reverse("taxi:driver-create"), data=data)
        created_user = get_user_model().objects.get(username=data["username"])
        self.assertEqual(created_user.username, data["username"])
        self.assertEqual(created_user.license_number, data["license_number"])
        self.assertEqual(created_user.first_name, data["first_name"])
        self.assertEqual(created_user.last_name, data["last_name"])
