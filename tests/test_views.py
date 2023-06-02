from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="n_1",
            country="c_1"
        )
        Manufacturer.objects.create(
            name="n_2",
            country="c_2"
        )
        Manufacturer.objects.create(
            name="n_3",
            country="c_3"
        )

    def test_retrieve_manufacturer(self):

        response = self.client.get(MANUFACTURER_URL)
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_form_initial_value(self):
        response = self.client.get(MANUFACTURER_URL)
        form = response.context["search_form"]

        self.assertEqual(form.initial["name"], "")

    def test_search_results(self):
        manufacturer1 = Manufacturer.objects.get(id=1)
        manufacturer2 = Manufacturer.objects.get(id=2)
        manufacturer3 = Manufacturer.objects.get(id=3)

        form_data = {"name": "n_1"}

        response = self.client.get(MANUFACTURER_URL, form_data)

        self.assertContains(response, manufacturer1.name)
        self.assertNotContains(response, manufacturer2.name)
        self.assertNotContains(response, manufacturer3.name)

    def test_no_search_results(self):
        form_data = {"name": "Mercedes"}
        response = self.client.get(MANUFACTURER_URL, form_data)

        self.assertContains(
            response,
            "There are no manufacturers in the service."
        )

    def test_search_few_results(self):
        manufacturer1 = Manufacturer.objects.get(id=1)
        manufacturer2 = Manufacturer.objects.get(id=2)
        manufacturer3 = Manufacturer.objects.get(id=3)

        form_data = {"name": "n_"}
        response = self.client.get(MANUFACTURER_URL, form_data)

        expected_names = [
            manufacturer1.name,
            manufacturer2.name,
            manufacturer3.name
        ]
        for name in expected_names:
            self.assertContains(response, name)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            username="u_1",
            first_name="n_1",
            last_name="c_1",
            license_number="LLL11111"
        )
        Driver.objects.create(
            username="u_2",
            first_name="n_2",
            last_name="c_2",
            license_number="LLL22222"
        )
        Driver.objects.create(
            username="u_3",
            first_name="n_3",
            last_name="c_3",
            license_number="LLL33333"
        )

    def test_retrieve_manufacturer(self):

        response = self.client.get(DRIVER_URL)
        driver_list = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_search_form_initial_value(self):
        response = self.client.get(DRIVER_URL)
        form = response.context["search_form"]

        self.assertEqual(form.initial["username"], "")

    def test_search_results(self):
        driver1 = Driver.objects.get(id=1)
        driver2 = Driver.objects.get(id=2)
        driver3 = Driver.objects.get(id=3)

        form_data = {"username": "u_1"}
        response = self.client.get(DRIVER_URL, form_data)

        self.assertContains(response, driver1.username)
        self.assertNotContains(response, driver2.username)
        self.assertNotContains(response, driver3.username)

    def test_no_search_results(self):
        form_data = {"username": "u_u"}
        response = self.client.get(DRIVER_URL, form_data)

        self.assertContains(response, "There are no drivers in the service.")

    def test_search_few_results(self):
        driver1 = Driver.objects.get(id=1)
        driver2 = Driver.objects.get(id=2)
        driver3 = Driver.objects.get(id=3)

        form_data = {"username": "u_"}
        response = self.client.get(DRIVER_URL, form_data)

        expected_names = [
            driver1.username,
            driver2.username,
            driver3.username
        ]
        for username in expected_names:
            self.assertContains(response, username)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        driver = Driver.objects.create(
            username="u_3",
            first_name="n_3",
            last_name="c_3",
            license_number="LLL33333"
        )
        manufacturer = Manufacturer.objects.create(
            name="n_1",
            country="c_1"
        )

        car1 = Car.objects.create(
            model="m_1",
            manufacturer=manufacturer,
        )
        car1.drivers.set([driver])

        car2 = Car.objects.create(
            model="m_2",
            manufacturer=manufacturer,
        )
        car2.drivers.set([driver])

        car3 = Car.objects.create(
            model="m_3",
            manufacturer=manufacturer,
        )
        car3.drivers.set([driver])

    def test_retrieve_car(self):

        response = self.client.get(CAR_URL)
        car_list = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )

    def test_search_form_initial_value(self):
        response = self.client.get(CAR_URL)
        form = response.context["search_form"]

        self.assertEqual(form.initial["model"], "")

    def test_search_results(self):
        car1 = Car.objects.get(id=1)
        car2 = Car.objects.get(id=2)
        car3 = Car.objects.get(id=3)

        form_data = {"model": "m_1"}
        response = self.client.get(CAR_URL, form_data)

        self.assertContains(response, car1.model)
        self.assertNotContains(response, car2.model)
        self.assertNotContains(response, car3.model)

    def test_no_search_results(self):
        form_data = {"model": "m_m"}
        response = self.client.get(CAR_URL, form_data)

        self.assertContains(response, "There are no cars in taxi")

    def test_search_few_results(self):
        car1 = Car.objects.get(id=1)
        car2 = Car.objects.get(id=2)
        car3 = Car.objects.get(id=3)

        form_data = {"model": "m_"}
        response = self.client.get(CAR_URL, form_data)

        expected_names = [
            car1.model,
            car2.model,
            car3.model
        ]
        for model in expected_names:
            self.assertContains(response, model)
