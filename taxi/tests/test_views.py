from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class TestIndexView(TestCase):
    def test_public_index(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_private_index(self):
        user = get_user_model().objects.create_user(
            username="test", password="1234"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )
        self.car = Car.objects.create(model="model", manufacturer=self.manufacturer)
        self.client.force_login(user)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)
        response2 = self.client.get(reverse("taxi:index"))
        self.assertEqual(response2.context["num_visits"], 2)
        self.assertTemplateUsed(response, "taxi/index.html")


class PublicAccessTests(TestCase):
    def test_login_required(self):
        responses = [
            self.client.get(CARS_URL),
            self.client.get(DRIVERS_URL),
            self.client.get(MANUFACTURERS_URL)
        ]
        for response in responses:
            self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1234",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Land Cruiser",
            manufacturer=manufacturer
        )

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_car_search(self):
        response = self.client.get(CARS_URL + "?model=Camry")
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Land Cruiser")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1234",
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="joyce.byers",
            first_name="Joyce",
            last_name="Byers",
            license_number="JOY26458"
        )
        Driver.objects.create(
            username="jim.hopper",
            first_name="Jim",
            last_name="Hopper",
            license_number="JIM26531"
        )

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVERS_URL)
        driver_list = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(driver_list))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_search(self):
        response = self.client.get(DRIVERS_URL + "?user_name=jim.hopper")
        self.assertContains(response, "jim.hopper")
        self.assertNotContains(response, "joyce.byers")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1234",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="German"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURERS_URL + "?name=BMW")
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")
