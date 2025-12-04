from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


# Create your tests here.
class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}"
                         )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create()
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        car_url = reverse("taxi:car-list")
        res = self.client.get(car_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        car_url = reverse("taxi:car-list")
        manufacturer = Manufacturer.objects.create()
        Car.objects.create(model="test",
                           manufacturer=manufacturer)
        Car.objects.create(model="test1",
                           manufacturer=manufacturer)
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        res = self.client.get(manufacturer_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(name="test")
        Manufacturer.objects.create(name="test1")
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        driver_url = reverse("taxi:driver-list")
        res = self.client.get(driver_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        driver_url = reverse("taxi:driver-list")
        Driver.objects.create(username="test",
                              license_number="QWE123456")
        Driver.objects.create(username="test1",
                              license_number="ASD456123")
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverSearchViewTest(TestCase):
    def setUp(self):

        Driver.objects.create(username="alice",
                              license_number="QWE123456")
        Driver.objects.create(username="bob",
                              license_number="ASD456123")
        Driver.objects.create(username="ALIce2",
                              license_number="ASD456124")
        Driver.objects.create(username="charlie",
                              license_number="QWE123457")
        self.user = get_user_model().objects.create_superuser(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_search_with_empty_query_returns_all_drivers(self):
        driver_url = reverse("taxi:driver-list")

        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)

        queryset = response.context["driver_list"]
        self.assertEqual(queryset.count(), 5)
        self.assertEqual(response.status_code, 200)

    def test_driver_search_by_username(self):
        driver_url = reverse("taxi:driver-list")
        response = self.client.get(
            driver_url,
            data={"username": "alice"},
        )
        queryset = response.context["driver_list"]
        returned_usernames = {driver.username for driver in queryset}
        self.assertEqual(returned_usernames, {"alice", "ALIce2"})
        self.assertEqual(response.status_code, 200)

    def test_driver_search_without_username(self):
        driver_url = reverse("taxi:driver-list")
        response = self.client.get(
            driver_url,
            data={"username": ""},
        )
        queryset = response.context["driver_list"]
        returned_usernames = {driver.username for driver in queryset}
        self.assertEqual(returned_usernames, {"alice",
                                              "ALIce2",
                                              "bob",
                                              "charlie",
                                              "user"})
        self.assertEqual(response.status_code, 200)


class CarSearchViewTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(model="ford",
                           manufacturer=manufacturer)
        Car.objects.create(model="Ford Fiesta",
                           manufacturer=manufacturer)
        Car.objects.create(model="Tesla",
                           manufacturer=manufacturer)
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_search_with_empty_query_returns_all_cars(self):
        car_url = reverse("taxi:car-list")
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        queryset = response.context["car_list"]
        self.assertEqual(queryset.count(), 3)
        self.assertEqual(response.status_code, 200)

    def test_car_search_by_model(self):
        car_url = reverse("taxi:car-list")
        response = self.client.get(
            car_url,
            data={"model": "ford"},
        )
        self.assertEqual(response.status_code, 200)
        queryset = response.context["car_list"]
        returned_models = {car.model for car in queryset}
        self.assertEqual(returned_models, {"ford", "Ford Fiesta"})
        self.assertEqual(response.status_code, 200)

    def test_car_search_without_model(self):
        car_url = reverse("taxi:car-list")
        response = self.client.get(
            car_url,
            data={"model": ""},
        )
        self.assertEqual(response.status_code, 200)
        queryset = response.context["car_list"]
        returned_models = {car.model for car in queryset}
        self.assertEqual(returned_models, {"ford",
                                           "Ford Fiesta",
                                           "Tesla"})
        self.assertEqual(response.status_code, 200)


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="toYota Motors")
        Manufacturer.objects.create(name="Mercedes-Benz")
        Manufacturer.objects.create(name="Ford")
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_search_with_empty_query_returns_all_manufacturers(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)
        queryset = response.context["manufacturer_list"]
        self.assertEqual(queryset.count(), 4)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search_by_name(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        response = self.client.get(
            manufacturer_url,
            data={"name": "Toyota"},
        )
        self.assertEqual(response.status_code, 200)
        queryset = response.context["manufacturer_list"]
        returned_manufacturers = {
            manufacturer.name for manufacturer in queryset
        }
        self.assertEqual(returned_manufacturers, {"Toyota",
                                                  "toYota Motors"})
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search_without_name(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        response = self.client.get(manufacturer_url,
                                   data={"name": ""})
        self.assertEqual(response.status_code, 200)
        queryset = response.context["manufacturer_list"]
        returned_manufacturers = {
            manufacturer.name for manufacturer in queryset
        }
        self.assertEqual(returned_manufacturers, {"Toyota",
                                                  "toYota Motors",
                                                  "Mercedes-Benz",
                                                  "Ford"})
        self.assertEqual(response.status_code, 200)
