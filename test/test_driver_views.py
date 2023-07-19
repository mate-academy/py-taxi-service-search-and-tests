from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import (
    Car,
    Manufacturer,
    Driver
)

CAR_LIST_URL = reverse("taxi:car-list")


class PublicDriverViewsTests(TestCase):

    def test_login_required_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[1])
        )
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_driver_create(self):
        response = self.client.get(
            reverse("taxi:driver-create")
        )
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_driver_license_update(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[1])
        )
        self.assertNotEquals(response.status_code, 200)


class PrivateCarViewsTests(TestCase):
    def setUp(self):

        self.user1 = get_user_model().objects.create_user(
            username="vasyl",
            password="password123",
            license_number="CBA54321"
        )
        self.user2 = get_user_model().objects.create_user(
            username="petro",
            password="password123",
            license_number="ABC12345"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="losos"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="corop"
        )
        self.car1 = Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer1,
        )
        self.car1.drivers.add(self.user2)
        self.car2 = Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer2,
        )
        self.car2.drivers.add(self.user1)
        self.client.force_login(self.user1)

    def test_retrieve_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["driver_list"]), list(drivers))

    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(f"{url}?username=vasyl")
        self.assertIn(self.user1, list(response.context["driver_list"]))
        self.assertNotIn(self.user2, list(response.context["driver_list"]))

    def test_retrieve_driver_detail(self):
        url = reverse("taxi:driver-detail", args=[self.user1.id])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["driver"], self.user1)

    def test_driver_license_update_view(self):

        url = reverse("taxi:driver-update", args=[self.user1.id])
        response = self.client.post(url, {"license_number": "GHD98745"})

        self.user1.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user1.license_number, "GHD98745")

    def test_driver_create_view(self):
        driver_data = {
            "username": "test3",
            "license_number": "GLD88888",
            "first_name": "vasyl",
            "last_name": "sydorenko",
            "password1": "asdgas1654651",
            "password2": "asdgas1654651",
        }
        url = reverse("taxi:driver-create")
        response = self.client.post(url, driver_data)

        self.assertEqual(response.status_code, 302)

        created_driver = get_user_model().objects.last()

        self.assertEqual(
            created_driver.license_number, driver_data["license_number"]
        )
        self.assertEqual(created_driver.first_name, driver_data["first_name"])
        self.assertEqual(created_driver.last_name, driver_data["last_name"])

    def test_driver_delete(self):
        url = reverse("taxi:driver-delete", args=[self.user1.id])
        self.client.post(url)
        self.assertFalse(
            get_user_model().objects.filter(id=self.car1.id).exists()
        )
