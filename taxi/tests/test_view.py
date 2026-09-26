from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class PrivateDriverSearchTest(TestCase):
    url = reverse("taxi:driver-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.john_smith = Driver.objects.create_user(
            username="john_smith",
            password="TestPass123!",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345",
        )

        cls.john_brown = Driver.objects.create_user(
            username="john_brown",
            password="TestPass123!",
            first_name="John",
            last_name="Brown",
            license_number="XYZ54321",
        )

        cls.michael_jones = Driver.objects.create_user(
            username="michael_jones",
            password="TestPass123!",
            first_name="Michael",
            last_name="Jones",
            license_number="QWE98765",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_returns_matching_drivers(self):
        res = self.client.get(self.url, {"username": "john"})
        self.assertCountEqual(
            [driver.username for driver in res.context["driver_list"]],
            ["john_smith", "john_brown"],
        )

    def test_search_is_case_insensitive(self):
        res = self.client.get(self.url, {"username": "JOHN_SMITH"})
        self.assertEqual(res.context["driver_list"][0].username, "john_smith")

    def test_search_returns_empty_queryset_when_no_matches_found(self):
        res = self.client.get(self.url, {"username": "bill"})
        self.assertQuerySetEqual(res.context["driver_list"], [])

    def test_search_returns_all_drivers_when_query_is_empty(self):
        res = self.client.get(self.url, {"username": ""})
        self.assertCountEqual(
            [driver.username for driver in res.context["driver_list"]],
            ["test_user", "john_smith", "john_brown", "michael_jones"],
        )


class PrivateCarSearchTest(TestCase):
    url = reverse("taxi:car-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.renault = Manufacturer.objects.create(
            name="Renault",
            country="France",
        )

        cls.megane = Car.objects.create(
            model="Megane", manufacturer=cls.renault
        )

        cls.clio = Car.objects.create(model="Clio", manufacturer=cls.renault)

        cls.x5 = Car.objects.create(model="X5", manufacturer=cls.bmw)

        cls.x6 = Car.objects.create(model="X6", manufacturer=cls.bmw)

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_returns_partial_model_match(self):
        res = self.client.get(self.url, {"model": "X"})
        self.assertCountEqual(
            [car.model for car in res.context["car_list"]], ["X5", "X6"]
        )

    def test_search_is_case_insensitive(self):
        res = self.client.get(self.url, {"model": "x"})
        self.assertCountEqual(
            [car.model for car in res.context["car_list"]], ["X5", "X6"]
        )

    def test_search_returns_empty_queryset_when_no_matches_found(self):
        res = self.client.get(self.url, {"model": "X7"})
        self.assertQuerySetEqual(res.context["car_list"], [])

    def test_search_returns_all_cars_when_query_is_empty(self):
        res = self.client.get(self.url, {"model": ""})
        self.assertCountEqual(
            [car.model for car in res.context["car_list"]],
            ["Megane", "Clio", "X5", "X6"],
        )


class PrivateManufacturerSearchTest(TestCase):
    url = reverse("taxi:manufacturer-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.alpine = Manufacturer.objects.create(
            name="Alpine",
            country="France",
        )

        cls.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        cls.tesla = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_returns_partial_name_match(self):
        res = self.client.get(self.url, {"name": "T"})
        self.assertCountEqual(
            [
                manufacturer.name
                for manufacturer in res.context["manufacturer_list"]
            ],
            ["Tesla", "Toyota"],
        )

    def test_search_is_case_insensitive(self):
        res = self.client.get(self.url, {"name": "t"})
        self.assertCountEqual(
            [
                manufacturer.name
                for manufacturer in res.context["manufacturer_list"]
            ],
            ["Tesla", "Toyota"],
        )

    def test_search_returns_empty_queryset_when_no_matches_found(self):
        res = self.client.get(self.url, {"name": "Bugatti"})
        self.assertQuerySetEqual(res.context["manufacturer_list"], [])

    def test_search_returns_all_manufacturers_when_query_is_empty(self):
        res = self.client.get(self.url, {"name": ""})
        self.assertCountEqual(
            [
                manufacturer.name
                for manufacturer in res.context["manufacturer_list"]
            ],
            ["Alpine", "Tesla", "Toyota", "BMW"],
        )


class CarDriverAssignmentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.car = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.user)
        self.url = reverse(
            "taxi:toggle-car-assign",
            args=[self.car.pk],
        )

    def test_assign_driver_to_car(self):
        self.client.get(self.url)

        self.assertIn(self.car, self.user.cars.all())

    def test_remove_driver_from_car(self):
        self.user.cars.add(self.car)

        self.client.get(self.url)

        self.assertNotIn(self.car, self.user.cars.all())


class CarCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.car = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "X6",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.user.pk],
            },
        )

        self.assertEqual(response.status_code, 302)

        car = Car.objects.get(model="X6")

        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertIn(self.user, car.drivers.all())

    def test_read_car(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.car)

    def test_update_car(self):
        response = self.client.post(
            reverse("taxi:car-update", args=[self.car.pk]),
            {
                "model": "X7",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.user.pk],
            },
        )

        self.assertEqual(response.status_code, 302)

        self.car.refresh_from_db()

        self.assertEqual(self.car.model, "X7")
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertIn(self.user, self.car.drivers.all())

    def test_delete_car(self):
        car_pk = self.car.pk

        response = self.client.post(reverse("taxi:car-delete", args=[car_pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=car_pk).exists())


class ManufacturerCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {
                "name": "Tesla",
                "country": "USA",
            },
        )

        self.assertEqual(response.status_code, 302)

        manufacturer = Manufacturer.objects.get(name="Tesla")

        self.assertEqual(manufacturer.country, "USA")

    def test_read_manufacturer(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.manufacturer, response.context["manufacturer_list"])

    def test_update_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.pk]),
            {
                "name": "Tesla",
                "country": "USA",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.manufacturer.refresh_from_db()

        self.assertEqual(self.manufacturer.name, "Tesla")
        self.assertEqual(self.manufacturer.country, "USA")

    def test_delete_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer.pk).exists()
        )


class DriverCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_driver(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "test_new_user",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "TST67890",
            },
        )

        self.assertEqual(response.status_code, 302)

        driver = Driver.objects.get(username="test_new_user")

        self.assertEqual(driver.license_number, "TST67890")

    def test_read_driver(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.user.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.user)

    def test_update_driver(self):
        response = self.client.post(
            reverse("taxi:driver-update", args=[self.user.pk]),
            {
                "license_number": "TST33333",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()

        self.assertEqual(self.user.license_number, "TST33333")

    def test_delete_driver(self):
        user_pk = self.user.pk

        response = self.client.post(
            reverse("taxi:driver-delete", args=[user_pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Driver.objects.filter(pk=user_pk).exists())
