from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from taxi.models import Car, Manufacturer


class PublicDriverDeleteFormTest(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password="password123"
        )

    def test_driver_delete_login_required(self):
        url = reverse("taxi:driver-delete", args=[str(self.test_user.id)])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="driver_1",
            password="best_driver_123",
            license_number="JAM12345",
        )
        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="VAG GROUP",
        )
        self.car = Car.objects.create(
            model="AUDI",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])

    def test_retrieve_drivers_list(self):
        url = reverse("taxi:driver-list")
        get_user_model().objects.create(
            username="driver_2",
            password="best_driver_also",
            license_number="ABC32145",
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_create_driver(self):
        form_data = {
            "username": "driver_2",
            "license_number": "ABC12345",
            "first_name": "Andrii",
            "last_name": "Yarotskiy",
            "password1": "django1234",
            "password2": "django1234",
        }

        res = self.client.post(reverse("taxi:driver-create"), data=form_data)
        self.assertEqual(res.status_code, 302)
        new_driver = get_user_model().objects.get(
            license_number=form_data["license_number"]
        )
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
        self.assertEqual(new_driver.username, form_data["username"])
        self.assertTrue(new_driver.check_password(form_data["password1"]))

    def test_search_drivers_by_username(self):
        get_user_model().objects.create_user(
            username="driver-2",
            password="django4321",
            license_number="ABC12345",
        )

        base_url = reverse("taxi:driver-list")
        query_string = urlencode({"username": "driver-2"})
        url = f"{base_url}?{query_string}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver-2")

        driver_list = response.context["driver_list"]
        self.assertTrue(any(d.username == "driver-2" for d in driver_list))
        self.assertFalse(any(d.username == "driver-1" for d in driver_list))

    def test_search_cars_by_model(self):
        base_url = reverse("taxi:car-list")
        query_string = urlencode({"model": "audi"})
        url = f"{base_url}?{query_string}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "audi")

        car_list = response.context["car_list"]
        self.assertTrue(any(d.model == "AUDI" for d in car_list))

    def test_search_manufacturer_by_name(self):
        base_url = reverse("taxi:manufacturer-list")
        query_string = urlencode({"name": "vag"})
        url = f"{base_url}?{query_string}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "vag")

        manufacturer_list = response.context["manufacturer_list"]
        self.assertTrue(any(d.name == "VAG GROUP" for d in manufacturer_list))
