from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

User = get_user_model()


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        self.assertEqual(str(manufacturer), manufacturer.name
                         + " " + manufacturer.country)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="hate_mercedes",
            first_name="Dmytro",
            last_name="Audi"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_car(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        car = Car.objects.create(model="M5", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)


class ManufacturerViewTests(TestCase):
    def setUp(self):
        self.manufacturer = (Manufacturer.objects.create
                             (name="BMW",
                              country="Germany"))
        self.user = (User.objects.create_user
                     (username="testuser",
                      password="testpass"))
        self.client.login(username="testuser",
                          password="testpass")

    def test_drivers_list_exists_url(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")

    def test_search_functionality(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"manufacturer": "BMW"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Ford")


class CarViewTests(TestCase):
    def setUp(self):
        self.manufacturer = (Manufacturer.objects.create
                             (name="BMW",
                              country="Germany"))
        self.car = Car.objects.create(model="M5",
                                      manufacturer=self.manufacturer)
        self.user = (User.objects.create_user
                     (username="testuser",
                      password="testpass"))
        self.client.login(username="testuser",
                          password="testpass")

    def test_cars_list_exists_url(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_functionality(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"manufacturer": "M5"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Ford")


class DriverViewTests(TestCase):
    def setUp(self):
        self.user = (User.objects.create_user
                     (username="testuser", password="testpass"))
        self.client.login(username="testuser", password="testpass")
        self.driver1 = (User.objects.create_user
                        (username="bmw_fan",
                         first_name="John",
                         last_name="Doe",
                         license_number="LICENSE123"))
        self.driver2 = (User.objects.create_user
                        (username="audi_fan",
                         first_name="Jane",
                         last_name="Smith",
                         license_number="LICENSE456"))

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_functionality(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "bmw_fan"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bmw_fan")


class TestSearchFeatures(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.driver1 = (Driver.objects.create
                        (username="hate_mercedes",
                         first_name="John",
                         last_name="Doe",
                         license_number="ABC12345"))

        self.manufacturer1 = (Manufacturer.objects.create
                              (name="BMW", country="Germany"))

        self.car1 = Car.objects.create(model="M5",
                                       manufacturer=self.manufacturer1)

    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-search"),
                                   {"driver": "John"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hate_mercedes")

    def test_manufacturer_search(self):
        response = self.client.get(reverse("taxi:car-search"),
                                   {"manufacturer": "BMW"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-search"),
                                   {"car": "M5"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "M5")
        self.assertNotContains(response, "M6")
