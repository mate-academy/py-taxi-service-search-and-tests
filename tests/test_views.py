from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

PK = 1

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[PK])
DRIVER_LIST_URL = reverse("taxi:driver-list")

TOGGLE_CAR_ASSIGN = reverse("taxi:toggle-car-assign", args=[PK])


class PublicCarTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        for i in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"manufacturer_name_{i}",
                country=f"manufacturer_country_{i}"
            )
            Car.objects.create(
                model=f"car_{i}",
                manufacturer=manufacturer
            )

        user = get_user_model().objects.create(
            username="test_username",
            password="test_pass123!",
            license_number="AAA12345"
        )
        self.client.force_login(user)

    def test_car_list_view(self):
        paginated_by = 5
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.select_related("manufacturer")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)[:paginated_by]
        )

    def test_search_car_by_model(self):
        searched_model = "car_1"
        response = self.client.get(CAR_LIST_URL, {"model": searched_model})

        self.assertEqual(
            response.context["car_list"][0],
            Car.objects.get(model=searched_model)
        )

    def test_retrieve_toggle_car_assign_add(self):
        self.client.get(TOGGLE_CAR_ASSIGN)

        response = self.client.get(CAR_DETAIL_URL)

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

        response = self.client.get(CAR_DETAIL_URL)

        car = Car.objects.get(id=PK)
        drivers_expected = car.drivers.all()
        drivers_actual = response.context["car"].drivers.all()

        self.assertEquals(
            list(drivers_actual),
            list(drivers_expected)
        )


class PublicManufacturerTests(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        for i in range(10):
            Manufacturer.objects.create(
                name=f"manufacturer_name_{i}",
                country=f"manufacturer_country_{i}"
            )

        user = get_user_model().objects.create(
            username="test_username",
            password="test_pass123!",
            license_number="AAA12345"
        )
        self.client.force_login(user)

    def test_all_manufacturers(self):
        paginated_by = 5
        response = self.client.get(MANUFACTURER_LIST_URL)
        cars = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(cars)[:paginated_by]
        )

    def test_search_manufacturer_by_name(self):
        searched_name = "manufacturer_name_1"
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": searched_name}
        )

        self.assertEqual(
            response.context["manufacturer_list"][0],
            Manufacturer.objects.get(name=searched_name)
        )


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        for i in range(10):
            get_user_model().objects.create(
                username=f"test_username{i}",
                password=f"test_pass12{i}!",
                license_number=f"AAA{i}2345"
            )

        user = get_user_model().objects.create(
            username="test_username",
            password="test_pass12!",
            license_number="AAA12346"
        )
        self.client.force_login(user)

    def test_all_drivers(self):
        paginated_by = 2
        response = self.client.get(DRIVER_LIST_URL)
        cars = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(cars)[:paginated_by]
        )

    def test_search_driver_by_username(self):
        searched_username = "test_username1"
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": searched_username}
        )

        self.assertEquals(
            response.context["driver_list"][0],
            get_user_model().objects.get(username=searched_username)
        )
