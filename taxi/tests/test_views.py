from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer_2 = Manufacturer.objects.create(
            name="test2",
            country="test2",
        )

        Car.objects.create(
            model="dfcdc",
            manufacturer=manufacturer_2,
        )
        Car.objects.create(
            model="motoycle",
            manufacturer=manufacturer_2,
        )

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car))

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_retrieve_manufacturer(self):

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )


class SearchViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123", license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2",
        )
        Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Tesla",
            manufacturer=manufacturer,
        )

        response = self.client.get(CAR_URL, {"model": "tes"})
        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Tesla")

    def test_search_driver(self):
        get_user_model().objects.create_user(
            username="admin",
            password="12345test",
            license_number="test123",
        )

        get_user_model().objects.create_user(
            username="test1user",
            password="123test",
            license_number="test1233",
        )

        response = self.client.get(DRIVER_URL, {"username": "ad"})
        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].license_number, "test123")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="test2",
            country="test2",
        )

        Manufacturer.objects.create(
            name="test3",
            country="test3",
        )

        response = self.client.get(MANUFACTURER_URL, {"name": "test2"})
        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "test2")


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="1234test",
        )

        self.client.force_login(self.user)

    def test_toggle_assign_to_car_add(self, **kwargs):
        manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2",
        )

        car = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )

        self.assertEqual(self.user.cars.count(), 0)
        self.client.post(
            reverse(
                "taxi:toggle-car-assign", kwargs={"pk": car.id}
            )
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.cars.count(), 1)

    def test_toggle_assign_to_car_remove(self, **kwargs):
        manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2",
        )

        car = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )

        self.user.cars.add(car)

        self.assertEqual(self.user.cars.count(), 1)
        self.client.post(
            reverse(
                "taxi:toggle-car-assign", kwargs={"pk": car.id}
            )
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.cars.count(), 0)


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test234",
        )
        self.client.force_login(self.user)

    def test_index(self):
        index_url = reverse("taxi:index")

        manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2",
        )
        Car.objects.create(model="BMW", manufacturer=manufacturer)

        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)

        cars = response.context["num_cars"]
        drivers = response.context["num_drivers"]
        manufacturers = response.context["num_manufacturers"]
        self.assertEqual(cars, 1)
        self.assertEqual(drivers, 1)
        self.assertEqual(manufacturers, 1)
        self.assertEqual(response.context["num_visits"], 1)
