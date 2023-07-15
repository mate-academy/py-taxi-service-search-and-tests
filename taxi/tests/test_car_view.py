from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

PK = "2"

CAR_LIST = reverse("taxi:car-list")
CAR_CREATE = reverse("taxi:car-create")
CAR_DETAIL = reverse("taxi:car-detail", args=[PK])
CAR_UPDATE = reverse("taxi:car-update", args=[PK])
CAR_DELETE = reverse("taxi:car-delete", args=[PK])

TOGGLE_CAR_ASSIGN = reverse("taxi:toggle-car-assign", args=[PK])


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Kingdom"
        )

        Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST)

        self.assertNotEquals(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(CAR_DETAIL)

        self.assertNotEquals(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(CAR_CREATE)

        self.assertNotEquals(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(CAR_UPDATE)

        self.assertNotEquals(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(CAR_DELETE)

        self.assertNotEquals(response.status_code, 200)

    def test_toggle_car_assign_login_required(self):
        response = self.client.get(TOGGLE_CAR_ASSIGN)

        self.assertNotEquals(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123456"
        )

        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test Kingdom"
        )

        for _ in range(3):
            Car.objects.create(
                model=f"Test model {_}",
                manufacturer=self.manufacturer
            )

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST)

        cars = Car.objects.select_related("manufacturer")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_search_by_model_car(self):
        Car.objects.create(
            model="New car",
            manufacturer=self.manufacturer
        )

        response = self.client.get(CAR_LIST + "?model=test")

        self.assertNotContains(response, "New car")
        self.assertContains(response, "name=\"model\" value=\"test\"")

    def test_search_by_name_pagination(self):
        for _ in range(15):
            Car.objects.create(
                model=f"New car {_}",
                manufacturer=self.manufacturer
            )

        response = self.client.get(CAR_LIST + "?model=new&page=2")

        self.assertNotContains(response, "Test model 1")
        self.assertContains(response, "name=\"model\" value=\"new\"")
        self.assertContains(response, "New car 5")

    def test_retrieve_car_detail(self):
        response = self.client.get(CAR_DETAIL)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_car_create(self):
        response = self.client.get(CAR_CREATE)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_car_update(self):
        response = self.client.get(CAR_UPDATE)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_car_delete(self):
        response = self.client.get(CAR_DELETE)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_toggle_car_assign_add(self):
        self.client.get(TOGGLE_CAR_ASSIGN)

        response = self.client.get(CAR_DETAIL)

        car = Car.objects.get(id=PK)
        drivers_expected = car.drivers.all()
        drivers_actual = response.context["car"].drivers.all()

        self.assertEquals(
            list(drivers_actual),
            list(drivers_expected)
        )

    def test_retrieve_toggle_car_assign_remove(self):
        for i in range(2):
            self.client.get(TOGGLE_CAR_ASSIGN)

        response = self.client.get(CAR_DETAIL)

        car = Car.objects.get(id=PK)
        drivers_expected = car.drivers.all()
        drivers_actual = response.context["car"].drivers.all()

        self.assertEquals(
            list(drivers_actual),
            list(drivers_expected)
        )
