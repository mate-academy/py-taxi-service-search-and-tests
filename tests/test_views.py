from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class UserCarManufacturer:
    def generate_data(self):
        self.user = get_user_model().objects.create(
            username="test_user",
            password="test24152",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Acura",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="MDX",
            manufacturer=self.manufacturer
        )


class NotLoginCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class LoginCarListTest(TestCase, UserCarManufacturer):
    def setUp(self) -> None:
        self.generate_data()
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)


class PublicCarListTests(TestCase, UserCarManufacturer):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class ToggleCarAssignTest(TestCase, UserCarManufacturer):
    def setUp(self) -> None:
        self.generate_data()
        self.client.force_login(self.user)

    def test_assign_new_driver_to_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.user.cars.all())

    def test_removed_driver_from_car(self):
        self.user.cars.add(self.car)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.user.cars.all())


class PublicManufacturerTest(TestCase):

    def test_manufacturers_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="country"
        )
        cls.manufacturer1 = Manufacturer.objects.create(
            name="test2",
            country="country"
        )
        cls.user1 = get_user_model().objects.create_user(
            username="test",
            password="t1e2s3t4",
            license_number="TST12452"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user1)

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
