from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class BaseViewTest:
    def assert_login_required(self, url_name):
        url = reverse(url_name)
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def create_and_login_user(self):
        user = get_user_model().objects.create_user(
            username="active_driver",
            password="password123",
            license_number="MAIN777"
        )
        self.client.login(username="active_driver", password="password123")
        return user


class DriverTests(BaseViewTest, TestCase):

    def test_login_required(self):
        self.assert_login_required("taxi:driver-list")

    def setUp(self):
        self.create_and_login_user()

        self.driver_mario = get_user_model().objects.create_user(
            username="mario_speedy",
            password="password123",
            first_name="Mario",
            last_name="Super",
            license_number="ASD11111"
        )
        self.driver_luigi = get_user_model().objects.create_user(
            username="luigi_green",
            password="password123",
            first_name="Luigi",
            last_name="Piper",
            license_number="ZXC22222"
        )

        self.URL = reverse("taxi:driver-list")

    def test_retrieve_drivers_page(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("driver_list", response.context)
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_search_driver_by_username_exact(self):
        response = self.client.get(
            self.URL,
            data={"search_query": "mario_speedy"}
        )
        self.assertIn(self.driver_mario, response.context["driver_list"])
        self.assertNotIn(self.driver_luigi, response.context["driver_list"])

    def test_search_driver_by_username_case_insensitive(self):
        response = self.client.get(self.URL, data={"search_query": "LUIGI"})
        self.assertIn(self.driver_luigi, response.context["driver_list"])
        self.assertNotIn(self.driver_mario, response.context["driver_list"])

    def test_search_driver_no_results(self):
        response = self.client.get(self.URL, data={"search_query": "bowser"})
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_driver_list_context_has_search_form(self):
        response = self.client.get(self.URL)
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(
            form.fields["search_query"].widget.attrs["placeholder"],
            "Search by username..."
        )


class ManufacturerTests(BaseViewTest, TestCase):

    def test_login_required(self):
        self.assert_login_required("taxi:manufacturer-list")

    def setUp(self):
        self.create_and_login_user()

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.URL = reverse("taxi:manufacturer-list")

    def test_retrieve_manufacturers_page(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_search_manufacturer_by_name_exact(self):
        response = self.client.get(self.URL, data={"search_query": "Toyota"})
        self.assertIn(
            self.manufacturer1,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer2,
            response.context["manufacturer_list"]
        )

    def test_search_manufacturer_by_name_case_insensitive(self):
        response = self.client.get(self.URL, data={"search_query": "tesla"})
        self.assertIn(
            self.manufacturer2,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer1,
            response.context["manufacturer_list"]
        )

    def test_search_manufacturer_no_results(self):
        response = self.client.get(self.URL, data={"search_query": "Ferrari"})
        self.assertEqual(
            len(response.context["manufacturer_list"])
            , 0
        )


class CarTests(BaseViewTest, TestCase):

    def test_login_required(self):
        self.assert_login_required("taxi:car-list")

    def setUp(self):
        self.create_and_login_user()

        self.audi = Manufacturer.objects.create(name="Audi", country="Germany")
        self.tesla = Manufacturer.objects.create(name="Tesla", country="USA")

        self.car_e_tron = Car.objects.create(
            model="e-tron",
            manufacturer=self.audi
        )
        self.car_model_s = Car.objects.create(
            model="Model S",
            manufacturer=self.tesla
        )

        self.URL = reverse("taxi:car-list")

    def test_retrieve_cars_page(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_search_car_by_model_exact(self):
        response = self.client.get(self.URL, data={"search_query": "e-tron"})
        self.assertIn(self.car_e_tron, response.context["car_list"])
        self.assertNotIn(self.car_model_s, response.context["car_list"])

    def test_search_car_no_results(self):
        response = self.client.get(self.URL, data={"search_query": "Lada"})
        self.assertEqual(len(response.context["car_list"]), 0)
