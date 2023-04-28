from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

URL_DRIVER_LIST = reverse("taxi:driver-list")
URL_CAR_LIST = reverse("taxi:car-list")
URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "Test_user",
            "1qazcde3",
        )

        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Firsttest",
            "last_name": "Lasttest",
            "license_number": "ADM56984",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class TestsSearchDrivers(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            "user1",
            "1qazcde3",
            license_number="ADE17865",
        )
        self.user2 = get_user_model().objects.create_user(
            "user2",
            "1qazcde3",
            license_number="ADX97235",
        )
        self.user3 = get_user_model().objects.create_user(
            "user3",
            "1qazcde3",
            license_number="ADX18235",
        )
        self.client.force_login(self.user3)

    def test_search_drivers_by_username(self):
        response = self.client.get(URL_DRIVER_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Driver List")

    def test_driver_search_form_valid(self):
        data = {"username": "user1"}
        response = self.client.get(URL_DRIVER_LIST, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")
        self.assertNotContains(response, "user2")

    def test_driver_search_form_invalid(self):
        data = {"username": "non_existing_user"}
        response = self.client.get(URL_DRIVER_LIST, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "user1")
        self.assertNotContains(response, "user2")
        self.assertContains(response, "There are no drivers in the service.")


class TestsSearchCars(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            "user1",
            "1qazcde3",
            license_number="ADE17865",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Accord 7",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="CRV",
            manufacturer=self.manufacturer,
        )

        self.client.force_login(self.user1)

    def test_search_car_by_model(self):
        response = self.client.get(URL_CAR_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Car List")

    def test_car_search_form_valid(self):
        data = {"model": "Accord 7"}
        response = self.client.get(URL_CAR_LIST, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Accord 7")
        self.assertNotContains(response, "CRV")

    def test_car_search_form_invalid(self):
        data = {"model": "non_existing_car"}
        response = self.client.get(URL_CAR_LIST, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Accord 7")
        self.assertNotContains(response, "CRV")
        self.assertContains(response, "There are no cars in taxi")


class TestsSearchManufacturer(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            "user1",
            "1qazcde3",
            license_number="ADE17865",
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )

        self.client.force_login(self.user1)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manufacturer List")

    def test_manufacturer_search_form_valid(self):
        data = {"name": "Honda"}
        response = self.client.get(URL_MANUFACTURER_LIST, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")
        self.assertNotContains(response, "Mazda")

    def test_manufacturer_search_form_invalid(self):
        data = {"name": "non_existing_car"}
        response = self.client.get(URL_MANUFACTURER_LIST, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "Mazda")
        self.assertContains(
            response,
            "There are no manufacturers in the service."
        )
