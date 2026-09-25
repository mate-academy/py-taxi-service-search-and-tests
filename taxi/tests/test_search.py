from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.tests.base import LoggedInTestCase

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class DriverSearchTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        drivers = (
            ("alice.smith", "Alice", "ALI12345"),
            ("alina.k", "Alina", "ALN12345"),
            ("bob.jones", "Alistair", "BOB12345"),
        )
        for username, first_name, license_number in drivers:
            get_user_model().objects.create_user(
                username=username,
                password="test12345",
                first_name=first_name,
                license_number=license_number,
            )

    def search(self, query):
        response = self.client.get(DRIVER_LIST_URL, {"username": query})
        drivers = response.context["driver_list"]
        return response, {driver.username for driver in drivers}

    def test_search_filters_drivers_by_username(self):
        _, usernames = self.search("ali")
        self.assertEqual(usernames, {"alice.smith", "alina.k"})

    def test_search_is_case_insensitive(self):
        _, usernames = self.search("ALI")
        self.assertEqual(usernames, {"alice.smith", "alina.k"})

    def test_search_does_not_look_at_other_fields(self):
        _, usernames = self.search("alistair")
        self.assertEqual(usernames, set())

    def test_empty_search_shows_all_drivers(self):
        _, usernames = self.search("")
        self.assertEqual(
            usernames, {"admin.user", "alice.smith", "alina.k", "bob.jones"}
        )

    def test_search_without_results_shows_message(self):
        response, usernames = self.search("nobody")
        self.assertEqual(usernames, set())
        self.assertContains(response, "No drivers found")

    def test_search_form_keeps_the_query(self):
        response, _ = self.search("ali")
        self.assertIn("search_form", response.context)
        self.assertContains(response, 'value="ali"')


class CarSearchTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        for model, manufacturer in (
            ("Focus", ford),
            ("Focus RS", ford),
            ("Mustang", ford),
            ("Yaris", toyota),
        ):
            Car.objects.create(model=model, manufacturer=manufacturer)

    def search(self, query):
        response = self.client.get(CAR_LIST_URL, {"model": query})
        models = {car.model for car in response.context["car_list"]}
        return response, models

    def test_search_filters_cars_by_model(self):
        _, models = self.search("focus")
        self.assertEqual(models, {"Focus", "Focus RS"})

    def test_search_is_case_insensitive(self):
        _, models = self.search("FOCUS")
        self.assertEqual(models, {"Focus", "Focus RS"})

    def test_search_does_not_look_at_manufacturer(self):
        _, models = self.search("ford")
        self.assertEqual(models, set())

    def test_empty_search_shows_all_cars(self):
        _, models = self.search("")
        self.assertEqual(models, {"Focus", "Focus RS", "Mustang", "Yaris"})

    def test_search_without_results_shows_message(self):
        response, models = self.search("tesla")
        self.assertEqual(models, set())
        self.assertContains(response, "No cars found")

    def test_search_form_keeps_the_query(self):
        response, _ = self.search("focus")
        self.assertIn("search_form", response.context)
        self.assertContains(response, 'value="focus"')


class ManufacturerSearchTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        for name, country in (
            ("Ford Motor", "USA"),
            ("Ferrari", "Italy"),
            ("BMW", "Germany"),
        ):
            Manufacturer.objects.create(name=name, country=country)

    def search(self, query):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": query})
        names = {
            manufacturer.name
            for manufacturer in response.context["manufacturer_list"]
        }
        return response, names

    def test_search_filters_manufacturers_by_name(self):
        _, names = self.search("f")
        self.assertEqual(names, {"Ford Motor", "Ferrari"})

    def test_search_is_case_insensitive(self):
        _, names = self.search("FERR")
        self.assertEqual(names, {"Ferrari"})

    def test_search_does_not_look_at_country(self):
        _, names = self.search("germany")
        self.assertEqual(names, set())

    def test_empty_search_shows_all_manufacturers(self):
        _, names = self.search("")
        self.assertEqual(names, {"Ford Motor", "Ferrari", "BMW"})

    def test_search_without_results_shows_message(self):
        response, names = self.search("tesla")
        self.assertEqual(names, set())
        self.assertContains(response, "No manufacturers found")

    def test_search_form_keeps_the_query(self):
        response, _ = self.search("ferr")
        self.assertIn("search_form", response.context)
        self.assertContains(response, 'value="ferr"')


class SearchPaginationTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        for number in range(1, 8):
            Car.objects.create(model=f"Corolla {number}", manufacturer=toyota)
        Car.objects.create(model="Yaris", manufacturer=toyota)

    def test_next_page_link_keeps_the_query(self):
        response = self.client.get(CAR_LIST_URL, {"model": "corolla"})
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertContains(response, 'href="?model=corolla&amp;page=2"')

    def test_second_page_shows_only_matching_cars(self):
        response = self.client.get(
            CAR_LIST_URL, {"model": "corolla", "page": 2}
        )
        models = [car.model for car in response.context["car_list"]]
        self.assertEqual(len(models), 2)
        self.assertTrue(all(model.startswith("Corolla") for model in models))

    def test_previous_page_link_keeps_the_query(self):
        response = self.client.get(
            CAR_LIST_URL, {"model": "corolla", "page": 2}
        )
        self.assertContains(response, 'href="?model=corolla&amp;page=1"')
