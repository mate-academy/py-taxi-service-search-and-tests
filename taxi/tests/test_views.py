from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class LoginRequiredTest(TestCase):
    def test_login_required_list_page(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_detail_page(self):
        driver = Driver.objects.create(
            username="Mykyta",
            license_number="AAA11111",
        )
        manufacturer = Manufacturer.objects.create(
            name="Renault",
            country="France",
        )
        car = Car.objects.create(model="Duster", manufacturer=manufacturer)

        res = self.client.get(reverse("taxi:driver-detail", args=[driver.pk]))
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(reverse("taxi:car-detail", args=[car.pk]))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_manufacturers_in_queryset_after_creation(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_cars_in_queryset_after_creation(self):
        manufacturer = Manufacturer.objects.create(name="Volkswagen")
        Car.objects.create(model="Arteon", manufacturer=manufacturer)
        Car.objects.create(model="Passat", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_drivers_in_queryset_after_creation(self):
        Driver.objects.create(username="Uklon", license_number="UKL11111")
        Driver.objects.create(username="Bolt", license_number="BLT11111")

        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class ManufacturerNameSearchTest(TestCase):
    def setUp(self):
        self.manufacturer_volks = Manufacturer.objects.create(
            name="Volkswagen",
        )
        self.manufacturer_ren = Manufacturer.objects.create(name="Renault")
        self.manufacturer_bmw = Manufacturer.objects.create(name="BMW")

        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123"
        )
        self.client.login(username="Mykyta", password="test123")

    def test_search_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "Renault"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Renault")
        self.assertNotContains(response, "Volkswagen")
        self.assertNotContains(response, "BMW")

    def test_search_one_letter(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "a"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volkswagen")
        self.assertContains(response, "Renault")
        self.assertNotContains(response, "BMW")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Audi"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There are no manufacturers in the service."
        )

    def test_empty_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volkswagen")
        self.assertContains(response, "Renault")
        self.assertContains(response, "BMW")


class CarModelSearchTest(TestCase):
    def setUp(self):
        self.manufacturer_volks = Manufacturer.objects.create(
            name="Volkswagen",
        )
        self.manufacturer_bmw = Manufacturer.objects.create(name="BMW")

        self.car1 = Car.objects.create(
            model="Arteon", manufacturer=self.manufacturer_volks
        )
        self.car2 = Car.objects.create(
            model="Passat", manufacturer=self.manufacturer_volks
        )
        self.car3 = Car.objects.create(
            model="330i", manufacturer=self.manufacturer_bmw
        )

        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123"
        )
        self.client.login(username="Mykyta", password="test123")

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Arteon"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arteon")
        self.assertNotContains(response, "Passat")
        self.assertNotContains(response, "330i")

    def test_search_one_letter(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "a"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arteon")
        self.assertContains(response, "Passat")
        self.assertNotContains(response, "330i")

    def test_search_no_results(self):
        response = self.client.get(reverse(
            "taxi:car-list"), {"model": "Polo"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars in taxi")

    def test_empty_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arteon")
        self.assertContains(response, "Passat")
        self.assertContains(response, "330i")

    def test_pagination_with_search(self):
        for index in range(10):
            Car.objects.create(
                model=f"Model{index}",
                manufacturer=self.manufacturer_bmw
            )

        response_first_page = self.client.get(
            reverse("taxi:car-list"), {"model": "Model", "page": 1}
        )
        self.assertEqual(response_first_page.status_code, 200)

        for index in range(5):
            self.assertContains(response_first_page, f"Model{index}")
            self.assertNotContains(response_first_page, f"Model{index + 5}")

        response_second_page = self.client.get(
            reverse("taxi:car-list"), {"model": "Model", "page": 2}
        )
        self.assertEqual(response_second_page.status_code, 200)

        for index in range(5, 10):
            self.assertContains(response_second_page, f"Model{index}")
            self.assertNotContains(response_second_page, f"Model{index - 5}")


class DriverUsernameSearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="uklon_driver",
            license_number="UKL11111",
        )
        self.driver2 = Driver.objects.create(
            username="bolt_driver",
            license_number="BLT11111",
        )
        self.driver3 = Driver.objects.create(
            username="uber_driver",
            license_number="UBR11111",
        )

        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123"
        )
        self.client.login(username="Mykyta", password="test123")

    def test_search_valid_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "uklon"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "uklon_driver")
        self.assertNotContains(response, "bolt_driver")
        self.assertNotContains(response, "uber_driver")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Taxi911"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "uklon_driver")
        self.assertNotContains(response, "bolt_driver")
        self.assertNotContains(response, "uber_driver")

    def test_search_empty_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "uklon_driver")
        self.assertContains(response, "bolt_driver")
        self.assertContains(response, "uber_driver")

    def test_search_second_section(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "driver"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "uklon_driver")
        self.assertContains(response, "bolt_driver")
        self.assertContains(response, "uber_driver")
