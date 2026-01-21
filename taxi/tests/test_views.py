from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class TestManufacturerViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser", password="<PASSWORD>"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="TestCountry"
        )

        self.urls = {
            "list": reverse("taxi:manufacturer-list"),
            "create": reverse("taxi:manufacturer-create"),
            "update": reverse(
                "taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk}
            ),
            "delete": reverse(
                "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk}
            ),
        }

    def test_login_required_manufacturer_list(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="TestCountry1"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="TestCountry2"
        )
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers),
            list(response.context["manufacturer_list"]),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="TestCountry1"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="TestCountry2"
        )
        response = self.client.get(self.urls["list"], {"name": "urer1"})
        manufacturer = response.context["manufacturer_list"]
        self.assertEqual(manufacturer[0].name, "Test Manufacturer1")


class TestDriverLoginRequiredViews(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            first_name="Test Driver",
            username="TestUsername",
            password="<PASSWORD>"
        )

        self.urls = {
            "list": reverse("taxi:driver-list"),
            "create": reverse("taxi:driver-create"),
            "update":
                reverse("taxi:driver-update", kwargs={"pk": self.driver.pk}),
            "delete":
                reverse("taxi:driver-delete", kwargs={"pk": self.driver.pk}),
            "detail":
                reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
            "assign":
                reverse(
                    "taxi:toggle-car-assign", kwargs={"pk": self.driver.pk}
            ),
        }

    def test_login_required_driver(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_driver_list(self):
        self.client.force_login(self.driver)
        Driver.objects.create(
            username="TestDriver1",
            password="<TESTPASSWORD1>",
            license_number="LICENSENUMBER1",
        )
        Driver.objects.create(
            username="TestDriver2",
            password="<TESTPASSWORD2>",
            license_number="LICENSENUMBER2",
        )
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(drivers),
            list(response.context["driver_list"]),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search(self):
        self.client.force_login(self.driver)
        Driver.objects.create(
            username="TestDriver1",
            password="<TESTPASSWORD1>",
            license_number="LICENSENUMBER1",
        )
        Driver.objects.create(
            username="TestDriver2",
            password="<TESTPASSWORD2>",
            license_number="LICENSENUMBER2",
        )
        response = self.client.get(self.urls["list"], {"username": "Driver1"})
        drivers = response.context["driver_list"]
        self.assertEqual(drivers[0].username, "TestDriver1")


class TestCarLoginRequiredViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser", password="<PASSWORD>"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="TestCountry"
        )
        self.car = Car.objects.create(
            model="Test Model", manufacturer=self.manufacturer
        )

        self.urls = {
            "list": reverse("taxi:car-list"),
            "create": reverse("taxi:car-create"),
            "update": reverse("taxi:car-update", kwargs={"pk": self.car.pk}),
            "delete": reverse("taxi:car-delete", kwargs={"pk": self.car.pk}),
            "detail": reverse("taxi:car-detail", kwargs={"pk": self.car.pk}),
        }

    def test_login_required_car(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_car_list(self):
        self.client.force_login(self.user)
        Car.objects.create(model="Model1", manufacturer=self.manufacturer)
        Car.objects.create(model="Model2", manufacturer=self.manufacturer)
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(cars),
            list(response.context["car_list"]),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search(self):
        self.client.force_login(self.user)
        Car.objects.create(model="Model1", manufacturer=self.manufacturer)
        Car.objects.create(model="Model2", manufacturer=self.manufacturer)
        response = self.client.get(self.urls["list"], {"model": "del1"})
        cars = response.context["car_list"]
        self.assertEqual(cars[0].model, "Model1")
