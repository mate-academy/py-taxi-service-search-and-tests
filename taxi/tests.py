from django.http import response
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from taxi.models import Manufacturer, Driver, Car
from django.db.utils import IntegrityError

from taxi.views import ManufacturerListView, DriverListView, CarListView

# ---------------------------------------------------------
# MODEL TESTS
# ---------------------------------------------------------

Login = "admin.user"
Password = "1qazcde3"


class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Dacia",
            country="Romania"
        )
        self.assertEqual(str(manufacturer), "Dacia Romania")

    def test_manufacturer_meta(self):
        self.assertEqual(Manufacturer._meta.ordering, ["name"])

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Dacia",
            country="Romania"
        )
        car = Car.objects.create(
            model="Duster",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "Duster")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Marianos",
            last_name="Dziad",
            first_name="Marek"
        )
        self.assertEqual(str(driver), "Marianos (Marek Dziad)")

    def test_driver_meta(self):
        self.assertEqual(
            Driver._meta.verbose_name,
            "driver"
        )
        self.assertEqual(
            Driver._meta.verbose_name_plural,
            "drivers"
        )

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(
            username="Marianos",

        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)


# ---------------------------------------------------------
# VIEVs TESTS
# ---------------------------------------------------------


class IndexViewTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="test12345"
        )

    def test_index_logout(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertEqual(res.status_code, 302)

    def test_index_login(self):
        self.client.login(username="testuser", password="test12345")
        res = self.client.get(reverse("taxi:index"))
        self.assertEqual(res.status_code, 200)

    def test_index_context(self):
        self.client.login(username="testuser", password="test12345")

        res = self.client.get(reverse("taxi:index"))

        self.assertEqual(res.context["num_drivers"], 12)
        self.assertEqual(res.context["num_cars"], 16)
        self.assertEqual(res.context["num_manufacturers"], 14)


class ManufacturerListViewTest(TestCase):
    TestCase.fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="test12345"
        )

    def test_manufacturer_list_view_logaut(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 302)

    def test_manufacturer_list_view_login(self):
        self.client.login(username="testuser", password="test12345")

        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_list_view_paginate(self):

        paginate_test = ManufacturerListView.paginate_by
        self.assertEqual(paginate_test, 5)

    def test_manufacturer_list_view_search(self):
        self.client.login(username="testuser", password="test12345")

        url = reverse("taxi:manufacturer-list") + "?name=BAIC"
        res = self.client.get(url)

        self.assertTrue(len(res.context["manufacturer_list"]) == 1)
        self.assertEqual(res.context["manufacturer_list"][0].name,
                         "BAIC"
                         )


class DriverListViewTestCase(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def test_driver_list_view_if_logaut(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 302)

    def test_driver_list_view_if_login(self):
        self.client.login(username=Login, password=Password)
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)

    def test_driver_list_view_paginate(self):
        paginate_test = DriverListView.paginate_by
        self.assertEqual(paginate_test, 5)

    def test_driver_list_view_search(self):
        self.client.login(username=Login, password=Password)

        url = reverse("taxi:driver-list") + "?username=jonathan.byers"
        res = self.client.get(url)

        self.assertEqual(res.context["driver_list"].count(), 1)
        self.assertEqual(res.context["driver_list"][0].username,
                         "jonathan.byers"
                         )


class CarListViewTestCase(TestCase):

    fixtures = ["taxi_service_db_data.json"]

    def test_car_list_view_if_logaut(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 302)

    def test_car_list_view_if_login(self):
        self.client.login(username=Login, password=Password)
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)

    def test_car_list_view_paginate(self):
        paginate_test = CarListView.paginate_by
        self.assertEqual(paginate_test, 5)

    def test_car_list_view_search(self):
        self.client.login(username=Login, password=Password)
        url = reverse("taxi:car-list") + "?model=Toyota"

        res = self.client.get(url)

        self.assertTrue(len(res.context["car_list"]) == 1)
        self.assertEqual(res.context["car_list"][0].model, "Toyota Yaris")

# ---------------------------------------------------------
# FORMs TESTS
# ---------------------------------------------------------


class DriverSearchFormTest(TestCase):
    def test_form_valid(self):
        form = DriverSearchForm(data={"username": "Marianoss"})

        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):

    def test_form_valid(self):
        form = CarSearchForm(data={"model": "Sandero"})

        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):

    def test_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Romunia"})

        self.assertTrue(form.is_valid())
