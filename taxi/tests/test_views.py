from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm
)
from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicAccessTest(TestCase):
    def test_login_required_for_all_protected_urls(self):
        urls_to_test = [
            MANUFACTURER_LIST_URL,
            CAR_LIST_URL,
            DRIVER_LIST_URL,
            reverse("taxi:index"),
            reverse("taxi:driver-detail", kwargs={"pk": 1}),
            reverse("taxi:car-detail", kwargs={"pk": 1}),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1}),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", kwargs={"pk": 1}),
            reverse("taxi:driver-delete", kwargs={"pk": 1}),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", kwargs={"pk": 1}),
            reverse("taxi:car-delete", kwargs={"pk": 1}),
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": 1}
            )
        ]

        for url in urls_to_test:
            with self.subTest(url=url):
                res = self.client.get(url)
                expected_redirect_url = f"/accounts/login/?next={url}"
                self.assertRedirects(res, expected_redirect_url)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="Test Country1"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Test Country2"
        )
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="test_user",
            password="",
        )
        self.client.force_login(self.driver1)
        self.driver2 = get_user_model().objects.create_user(
            username="joyce.byers",
            password="",
            first_name="Joyce",
            last_name="Byers",
            license_number="JOY12345",
        )

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Factory",
            country="Test Country"
        )
        self.car1 = Car.objects.create(
            model="Test Car1",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Test Car2",
            manufacturer=self.manufacturer,
        )

    def test_retrieve_cars(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_count_visit(self):
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertEqual(res.context["num_visits"], 1)
        res = self.client.get(url)
        self.assertEqual(res.context["num_visits"], 2)


class PrivateCarAssignTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Factory",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer,
        )

    def test_assign_driver_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        res = self.client.get(url)
        expected_url = reverse("taxi:car-detail", args=[self.car.id])
        self.assertRedirects(res, expected_url)
        self.assertIn(self.car, self.user.cars.all())

    def test_remove_driver_from_car(self):
        self.user.cars.add(self.car)
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        res = self.client.get(url)
        expected_url = reverse("taxi:car-detail", args=[self.car.id])
        self.assertRedirects(res, expected_url)
        self.assertNotIn(self.car, self.user.cars.all())


class PrivateCarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Factory",
            country="Test Country"
        )
        self.car_tesla = Car.objects.create(
            model="Tesla Model S",
            manufacturer=self.manufacturer,
        )
        self.car_toyota = Car.objects.create(
            model="Toyota Camry",
            manufacturer=self.manufacturer,
        )

    def test_search_form_in_context(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertIsInstance(res.context["search_form"], CarModelSearchForm)

    def test_search_without_parameters_returns_all(self):
        res = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 2)
        self.assertIn(self.car_tesla, res.context["car_list"])
        self.assertIn(self.car_toyota, res.context["car_list"])

    def test_successful_search_by_model(self):
        res = self.client.get(CAR_LIST_URL, {"model": "Tes"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 1)
        self.assertIn(self.car_tesla, res.context["car_list"])
        self.assertNotIn(self.car_toyota, res.context["car_list"])

    def test_search_with_no_results(self):
        res = self.client.get(CAR_LIST_URL, {"model": "BMW"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 0)


class PrivateManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)
        self.manufacturer_toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer_tesla = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_search_form_in_context(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertIsInstance(
            res.context["search_form"],
            ManufacturerNameSearchForm
        )

    def test_search_without_parameters_returns_all(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 2)
        self.assertIn(
            self.manufacturer_toyota,
            res.context["manufacturer_list"]
        )
        self.assertIn(
            self.manufacturer_tesla,
            res.context["manufacturer_list"]
        )

    def test_successful_search_by_name(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "Tes"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 1)
        self.assertIn(
            self.manufacturer_tesla,
            res.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer_toyota,
            res.context["manufacturer_list"]
        )

    def test_search_with_no_results(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "BMW"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 0)


class PrivateDriverSearchTest(TestCase):
    def setUp(self):
        self.driver_joyce = get_user_model().objects.create_user(
            username="joyce.byers",
            password="",
            first_name="Joyce",
            last_name="Byers",
            license_number="JOY12345",
        )
        self.client.force_login(self.driver_joyce)
        self.driver_jim = get_user_model().objects.create_user(
            username="jim.hopper",
            password="",
            first_name="Jim",
            last_name="Hopper",
            license_number="JIM12345",
        )

    def test_search_form_in_context(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertIsInstance(
            res.context["search_form"],
            DriverUsernameSearchForm
        )

    def test_search_without_parameters_returns_all(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 2)
        self.assertIn(self.driver_joyce, res.context["driver_list"])
        self.assertIn(self.driver_jim, res.context["driver_list"])

    def test_successful_search_by_username(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "jim"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 1)
        self.assertIn(self.driver_jim, res.context["driver_list"])
        self.assertNotIn(self.driver_joyce, res.context["driver_list"])

    def test_search_with_no_results(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "mariia"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 0)
        self.assertNotIn(self.driver_joyce, res.context["driver_list"])
        self.assertNotIn(self.driver_jim, res.context["driver_list"])
