from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicViewsTest(TestCase):
    def test_login_required(self):
        for url in [MANUFACTURER_URL, CAR_URL, DRIVER_URL]:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="VAG")
        Manufacturer.objects.create(name="BMW")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "VAG",
            "country": "Germany",
        }
        self.client.post(reverse("taxi:manufacturer-create"), form_data)
        manufacturer = Manufacturer.objects.get(name="VAG")
        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])

    def test_retrieve_drivers(self):
        Driver.objects.create(username="test1",
                              password="<PASSWORD>",
                              license_number="BTC12345")
        Driver.objects.create(username="test2",
                              password="<PASSWORD>",
                              license_number="BCC12545")
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers))
        self.assertTemplateUsed(response,
                                "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test1",
            "password1": "1A2g3s4f1234",
            "password2": "1A2g3s4f1234",
            "first_name": "test",
            "last_name": "test",
            "license_number": "DDD12345",
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        driver = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(driver.first_name, form_data["first_name"])
        self.assertEqual(driver.last_name, form_data["last_name"])
        self.assertEqual(driver.license_number, form_data["license_number"])

    def test_retrieve_cars(self):
        Car.objects.create(model="BMW",
                           manufacturer=Manufacturer.objects.create(
                               name="BMW"
                           ))
        Car.objects.create(model="Audi",
                           manufacturer=Manufacturer.objects.create(
                               name="VAG"
                           ))
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))
        self.assertTemplateUsed(response,
                                "taxi/car_list.html")

    def test_create_car(self):
        form_data = {
            "model": "pas",
            "manufacturer": Manufacturer.objects.create(name="Vag").id,
            "drivers": Driver.objects.create(username="test1",
                                             license_number="DDD12345").id,
        }
        self.client.post(reverse("taxi:car-create"), form_data)
        car = Car.objects.get(model="pas")
        self.assertEqual(car.model, form_data["model"])
        self.assertEqual(car.manufacturer.id, form_data["manufacturer"])


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.driver1 = Driver.objects.create(username="john_doe",
                                             license_number="ABC12345")
        self.driver2 = Driver.objects.create(username="jane_doe",
                                             license_number="XYZ98765")
        self.driver3 = Driver.objects.create(username="doe_john",
                                             license_number="LMN56789")

    def test_search_form_no_results(self):
        response = self.client.get(DRIVER_URL, {"username": "not_found"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["driver_list"], [])

    def test_search_form_partial_match(self):
        response = self.client.get(DRIVER_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 2)
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertIn(self.driver3, response.context["driver_list"])

    def test_search_form_full_match(self):
        response = self.client.get(DRIVER_URL, {"username": "jane_doe"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertIn(self.driver2, response.context["driver_list"])

    def test_filtered_search_results_by_driver(self):
        response = self.client.get(DRIVER_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 2)
        self.assertEqual(list(response.context["driver_list"]),
                         list(Driver.objects.filter(
                             username__contains="john").order_by("id")))


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Mitsubishi")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota")
        self.manufacturer3 = Manufacturer.objects.create(
            name="Mazda")

    def test_search_form_no_results(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "Lexus"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["manufacturer_list"], [])

    def test_search_form_partial_match(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertIn(self.manufacturer1,
                      response.context["manufacturer_list"])
        self.assertIn(self.manufacturer3,
                      response.context["manufacturer_list"])

    def test_search_form_full_match(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertIn(self.manufacturer2,
                      response.context["manufacturer_list"])

    def test_filtered_search_results_by_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(Manufacturer.objects.filter(
                             name__contains="M").order_by("name")))


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.car1 = Car.objects.create(
            model="Mitsubishi Lancer",
            manufacturer=Manufacturer.objects.create(name="Mitsubishi"),
        )
        self.car2 = Car.objects.create(
            model="Ford Focus",
            manufacturer=Manufacturer.objects.create(name="Ford"),
        )
        self.car3 = Car.objects.create(
            model="Mazda 3",
            manufacturer=Manufacturer.objects.create(name="Mazda"),
        )

    def test_search_form_no_results(self):
        response = self.client.get(CAR_URL, {"model": "Lexus"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["car_list"], [])

    def test_search_form_partial_match(self):
        response = self.client.get(CAR_URL, {"model": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertIn(self.car1,
                      response.context["car_list"])
        self.assertIn(self.car3,
                      response.context["car_list"])

    def test_search_form_full_match(self):
        response = self.client.get(CAR_URL, {"model": "Ford"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertIn(self.car2,
                      response.context["car_list"])

    def test_filtered_search_results_by_car(self):
        response = self.client.get(CAR_URL, {"model": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertEqual(list(response.context["car_list"]),
                         list(Car.objects.filter(
                             model__contains="M").order_by("id")))
