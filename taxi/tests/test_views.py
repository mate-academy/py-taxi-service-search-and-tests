from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class TestViewsStatusCode(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(HOME_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_page_status_code(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_page_status_code(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_cars_page_status_code(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class TestDriversListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        get_user_model().objects.create_user(
            username="admin2",
            password="admin2",
            license_number="JON26231",
        )
        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["object_list"]), list(drivers))


class TestToggleAssignToCar(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
            license_number="JON26231",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(
            model="A6", manufacturer=self.manufacturer
        )

    def test_toggle_assign_to_car_when_not_assigned(self):
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car in self.user.cars.all())

    def test_toggle_assign_to_car_when_already_assigned(self):
        self.car.drivers.add(self.user)
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.car in self.user.cars.all())
