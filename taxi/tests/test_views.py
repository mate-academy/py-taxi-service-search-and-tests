import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import response
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturer(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturer(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCar(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCar(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="I8",
            manufacturer=self.manufacturer,
        )
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class SearchResultsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

        self.name1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.name2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.driver1 = get_user_model().objects.create(
            license_number=str(uuid.uuid4())[:8],
            username="user1",
        )
        self.driver2 = get_user_model().objects.create(
            license_number=str(uuid.uuid4())[:8],
            username="user2",
        )

        self.car1 = Car.objects.create(
            model="I8",
            manufacturer=self.name1,
        )
        self.car2 = Car.objects.create(
            model="X5",
            manufacturer=self.name2,
        )
        self.car1.drivers.add(self.driver1)
        self.car2.drivers.add(self.driver2)

    def test_search_car(self):
        res = self.client.get(
            reverse("taxi:car-list"), {"model": "I8"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car1.model)
        self.assertNotContains(res, self.car2.model)

    def test_search_manufacturer(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Audi"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.name1.name)
        self.assertNotContains(res, self.name2.name)

    def test_search_driver(self):
        res = self.client.get(
            reverse("taxi:driver-list"), {"username": "user1"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.driver1.username)
        self.assertNotContains(res, self.driver2.username)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "QWE12345",

        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, "Test first")
        self.assertEqual(new_user.last_name, "Test last")
        self.assertEqual(new_user.license_number, "QWE12345")
