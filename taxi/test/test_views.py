from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="password123",
            license_number="TST00000"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="TestMan", country="UA")
        Car.objects.create(
            model="TestCar",
            manufacturer=Manufacturer.objects.first()
        )
        self.driver_count = Driver.objects.count()

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_context_data(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_drivers"], self.driver_count)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)


class PrivateDriverTests(TestCase):
    """Test authenticated driver access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        """Test retrieving driver list"""
        get_user_model().objects.create_user(
            username="driver1",
            password="test12345",
            license_number="DEF12345"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="test12345",
            license_number="GHI12345"
        )

        res = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_drivers_by_username(self):
        """Test searching drivers by username"""
        get_user_model().objects.create_user(
            username="john_doe",
            password="test12345",
            license_number="JOH12345"
        )
        get_user_model().objects.create_user(
            username="jane_smith",
            password="test12345",
            license_number="JAN12345"
        )

        res = self.client.get(DRIVER_LIST_URL, {"username": "john"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 1)
        self.assertEqual(
            res.context["driver_list"][0].username,
            "john_doe"
        )

    def test_search_drivers_no_results(self):
        """Test searching with no matching results"""
        res = self.client.get(DRIVER_LIST_URL, {"username": "nonexistent"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 0)


class PrivateCarTests(TestCase):
    """Test authenticated car access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_retrieve_cars(self):
        """Test retrieving car list"""
        Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Model 3",
            manufacturer=self.manufacturer
        )

        res = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )

    def test_search_cars_by_model(self):
        """Test searching cars by model"""
        Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Model 3",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Roadster",
            manufacturer=self.manufacturer
        )

        res = self.client.get(CAR_LIST_URL, {"model": "model"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 2)

    def test_search_cars_case_insensitive(self):
        """Test that search is case-insensitive"""
        Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

        res = self.client.get(CAR_LIST_URL, {"model": "MODEL"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 1)


class PrivateManufacturerTests(TestCase):
    """Test authenticated manufacturer access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        """Test retrieving manufacturer list"""
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        res = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_manufacturers_by_name(self):
        """Test searching manufacturers by name"""
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Mercedes", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "b"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 1)
        self.assertEqual(
            res.context["manufacturer_list"][0].name,
            "BMW"
        )


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="user1",
            password="pwd",
            license_number="USR12345"
        )
        self.other_driver = Driver.objects.create_user(
            username="user2",
            password="pwd",
            license_number="USR54321"
        )
        self.client.force_login(self.user)
        self.man = Manufacturer.objects.create(name="Man", country="UA")
        self.car = Car.objects.create(model="Car1", manufacturer=self.man)
        self.url = reverse("taxi:toggle-car-assign", args=[self.car.pk])

    def test_assign_to_car(self):
        self.assertNotIn(self.car, self.user.cars.all())
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertIn(self.car, self.user.cars.all())

    def test_unassign_from_car(self):
        self.user.cars.add(self.car)
        self.assertIn(self.car, self.user.cars.all())
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertNotIn(self.car, self.user.cars.all())
