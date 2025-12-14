from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer


User = get_user_model()


class CarSearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        # Create manufacturers
        cls.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.ford = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        # Create cars
        cls.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=cls.toyota
        )
        cls.car2 = Car.objects.create(
            model="Camry",
            manufacturer=cls.toyota
        )
        cls.car3 = Car.objects.create(
            model="Focus",
            manufacturer=cls.ford
        )

    def setUp(self):
        # Log in before each test
        self.client.login(username="testuser", password="password")

    def test_search_by_existing_model_name(self):
        """Search by model returns correct cars"""
        url = reverse("taxi:car-list") + "?search=c"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)

    def test_search_by_nonexistent_model_name(self):
        """Searching for a model that doesn't exist returns no result"""
        url = reverse("taxi:car-list") + "?search=BMW"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["object_list"], [])

    def test_search_without_parameter(self):
        """No search parameter returns all cars"""
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["object_list"],
            [self.car1, self.car2, self.car3],
            ordered=False,
        )


class DriverSearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User for login
        cls.driver1 = User.objects.create_user(
            username="alice", password="pass", license_number="LIC-1001"
        )
        cls.driver2 = User.objects.create_user(
            username="bob", password="pass", license_number="LIC-1002"
        )
        cls.driver3 = User.objects.create_user(
            username="charlie", password="pass", license_number="LIC-1003"
        )

    def setUp(self):
        # log in test user
        self.client.login(username="alice", password="pass")

    def test_search_by_existing_username(self):
        url = reverse("taxi:driver-list") + "?search=alice"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertNotContains(response, self.driver3.username)

    def test_search_by_partial_username(self):
        url = reverse("taxi:driver-list") + "?search=bo"
        response = self.client.get(url)
        drivers = response.context["object_list"]

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver2, drivers)  # bob
        self.assertNotIn(self.driver1, drivers)  # alice
        self.assertNotIn(self.driver3, drivers)

    def test_search_without_parameter(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["object_list"],
            [self.driver1, self.driver2, self.driver3],
            ordered=False,
        )


class ManufacturerSearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # user for login
        cls.user = User.objects.create_user(
            username="testuser", password="password", license_number="TEST-001"
        )

        # manufacturers
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        cls.manufacturer3 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def setUp(self):
        self.client.login(username="testuser", password="password")

    def test_search_by_existing_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=Toy")

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["object_list"]

        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)
        self.assertNotIn(self.manufacturer3, manufacturers)

    def test_search_without_parameter(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["object_list"]

        self.assertEqual(list(manufacturers), list(Manufacturer.objects.all()))

    def test_search_with_non_existing_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=Tesla")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)


class CarDriverRelationTests(TestCase):

    def test_driver_assigned_to_car(self):
        driver = User.objects.create_user(
            username="driver", password="pass", license_number="LIC-200"
        )

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        car = Car.objects.create(model="X5", manufacturer=manufacturer)

        car.drivers.add(driver)

        self.assertIn(driver, car.drivers.all())


class ManufacturerAccessTests(TestCase):

    def test_create_requires_login(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertEqual(response.status_code, 302)
