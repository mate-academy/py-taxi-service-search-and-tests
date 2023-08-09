from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[1])
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_DELETE_URL = reverse("taxi:car-delete", args=[1])
CAR_UPDATE_URL = reverse("taxi:car-update", args=[1])
TOGGLE_ASSIGN_TO_CAR_URL = reverse("taxi:toggle-car-assign", args=[1])


class PublicCarTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(CAR_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(CAR_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(CAR_DELETE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(CAR_UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "TestUser",
            "TestPassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)
        car = Car.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["car"],
            car
        )
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_toggle_assign_to_car(self):
        car = Car.objects.get(id=1)
        car.drivers.add(self.user)
        self.client.get(TOGGLE_ASSIGN_TO_CAR_URL)

        self.assertFalse(car in self.user.cars.all())

        self.client.get(TOGGLE_ASSIGN_TO_CAR_URL)
        self.assertTrue(car in self.user.cars.all())
