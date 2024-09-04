from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Volkswagen")
        Manufacturer.objects.create(name="Skoda")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        manufacturer = Manufacturer.objects.create(name="Volkswagen")
        car = Car.objects.create(model="Floride", manufacturer=manufacturer)

        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)
        res2 = self.client.get(reverse("taxi:car-detail", args=[car.pk]))
        self.assertNotEqual(res2.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="Volkswagen")
        Car.objects.create(model="Floride", manufacturer=manufacturer)
        Car.objects.create(model="X5 M", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        driver = Driver.objects.create(
            username="Adam", license_number="ZXC12345"
        )

        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)
        res2 = self.client.get(reverse("taxi:driver-detail", args=[driver.pk]))
        self.assertNotEqual(res2.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(username="Adam", license_number="ZXC12345")
        Driver.objects.create(username="Eve", license_number="ASD54321")
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class ManufacturerNameSearchTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Volkswagen")
        self.manufacturer2 = Manufacturer.objects.create(name="Skoda")
        self.manufacturer3 = Manufacturer.objects.create(name="BMW")

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "Volkswagen"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volkswagen")
        self.assertNotContains(response, "Skoda")
        self.assertNotContains(response, "BMW")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Ford"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There are no manufacturers in the service."
        )

    def test_search_partial_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "Volk"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volkswagen")
        self.assertNotContains(response, "Skoda")
        self.assertNotContains(response, "BMW")

    def test_empty_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volkswagen")
        self.assertContains(response, "Skoda")
        self.assertContains(response, "BMW")


class CarModelSearchTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda")

        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Accord", manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Civic", manufacturer=self.manufacturer2
        )

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Accord")
        self.assertNotContains(response, "Civic")

    def test_search_no_results(self):
        response = self.client.get(reverse(
            "taxi:car-list"), {"model": "Focus"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars in taxi")

    def test_search_partial_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Civ"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Accord")

    def test_empty_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Accord")
        self.assertContains(response, "Civic")

    def test_pagination_with_search(self):
        for index in range(10):
            Car.objects.create(model=f"Model{index}",
                               manufacturer=self.manufacturer1)

        response_first_page = self.client.get(
            reverse("taxi:car-list"), {"model": "Model", "page": 1}
        )
        self.assertEqual(response_first_page.status_code, 200)
        for index in range(5):
            self.assertContains(response_first_page, f"Model{index}")
        for index in range(5, 10):
            self.assertNotContains(response_first_page, f"Model{index}")

        response_second_page = self.client.get(
            reverse("taxi:car-list"), {"model": "Model", "page": 2}
        )
        self.assertEqual(response_second_page.status_code, 200)
        for index in range(5, 10):
            self.assertContains(response_second_page, f"Model{index}")
        for index in range(5):
            self.assertNotContains(response_second_page, f"Model{index}")


class DriverUsernameSearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(username="john_doe",
                                             license_number="QWE12345")
        self.driver2 = Driver.objects.create(username="jane_smith",
                                             license_number="ASD23456")
        self.driver3 = Driver.objects.create(username="johnny_bravo",
                                             license_number="ZXC34567")

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_valid_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "john"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertContains(response, "johnny_bravo")
        self.assertNotContains(response, "jane_smith")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Usyk"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")
        self.assertNotContains(response, "johnny_bravo")

    def test_search_empty_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertContains(response, "jane_smith")
        self.assertContains(response, "johnny_bravo")

    def test_search_partial_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "smith"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jane_smith")
        self.assertNotContains(response, "john_doe")
        self.assertNotContains(response, "johnny_bravo")
