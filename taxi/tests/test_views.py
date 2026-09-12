from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicTaxiTests(TestCase):
    def test_car_return_to_anonymous(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_return_to_anonymous(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_return_to_anonymous(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaxiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        manufacturer = Manufacturer.objects.create(name="JAC", country="China")
        Car.objects.create(model="JAC", manufacturer=manufacturer)
        Driver.objects.create(
            username="Test User",
            first_name="Test",
            last_name="User",
            license_number="ACB12345"
        )
        self.client.force_login(self.user)

    def test_car_list_opened(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all()),
        )

    def test_driver_list_opened(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all()),
        )

    def test_manufacturer_list_opened(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )


class SearchTaxiTests(TestCase):
    def setUp(self):
        self.user1 = Driver.objects.create_user(
            username="john_malkovich",
            password="test1234",
            license_number="ABC12345",
        )
        self.user2 = Driver.objects.create_user(
            username="adam_malkovich",
            password="test1235",
            license_number="ABC12346",
        )
        self.user3 = Driver.objects.create_user(
            username="user_tester",
            password="test1236",
            license_number="ABC12347",
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="test_w",
            country="test_country"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test_x",
            country="test_village"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="JAC",
            country="China"
        )
        self.car1 = Car.objects.create(
            model="model_x",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="model_y",
            manufacturer=self.manufacturer2,
        )
        self.car3 = Car.objects.create(
            model="JS8",
            manufacturer=self.manufacturer3,
        )
        self.client.force_login(self.user1)

    def test_driver_search(self):
        response = self.client.get(DRIVER_URL, {"username": "mal"})
        result = Driver.objects.filter(username__icontains="mal")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(result),
        )

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "test"})
        result = Manufacturer.objects.filter(name__icontains="test")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(result),
        )

    def test_car_search(self):
        response = self.client.get(CAR_URL, {"model": "model"})
        result = Car.objects.filter(model__icontains="model")
        self.assertEqual(
            list(response.context["car_list"]),
            list(result),
        )

    def test_empty_search(self):
        response = self.client.get(DRIVER_URL, {"username": ""})
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all()),
        )

    def test_empty_search_without_parameters(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all()),
        )
