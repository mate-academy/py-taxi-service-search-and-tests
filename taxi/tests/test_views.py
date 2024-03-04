from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicViewTest(TestCase):
    def test_login_required(self):
        urls = [
            CAR_URL,
            DRIVER_URL,
            MANUFACTURER_URL
        ]
        for url in urls:
            self.assertNotEqual(
                self.client.get(url).status_code, 200
            )


class PrivateViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )
        self.test_password = "testPass1"
        self.user = get_user_model().objects.create_user(
            username="admin.test",
            license_number="ADM12345",
            first_name="Administrator",
            last_name="Test",
            password=self.test_password
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_search_by_valid_model(self):
        test_model = "test1"
        Car.objects.create(model=test_model, manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL + f"?model={test_model}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertContains(
            response,
            test_model
        )

    def test_car_search_by_invalid_model(self):
        response = self.client.get(CAR_URL + "?model=notValid")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_car_empty_search(self):
        response = self.client.get(CAR_URL + "?model=")
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_manufacturer_search_by_valid_name(self):
        test_name = "test1"
        Manufacturer.objects.create(name=test_name)
        response = self.client.get(MANUFACTURER_URL + f"?name={test_name}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertContains(
            response,
            test_name
        )

    def test_manufacturer_search_by_invalid_name(self):
        response = self.client.get(MANUFACTURER_URL + "?name=notValid")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_manufacturer_empty_search(self):
        response = self.client.get(MANUFACTURER_URL + "?name=")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_driver_search_by_valid_username(self):
        test_username = "test1"
        get_user_model().objects.create(
            username=test_username,
            password=self.test_password
        )
        response = self.client.get(DRIVER_URL + f"?username={test_username}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertContains(
            response,
            test_username
        )

    def test_driver_search_by_invalid_username(self):
        response = self.client.get(DRIVER_URL + "?username=notValid")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_driver_empty_search(self):
        response = self.client.get(DRIVER_URL + "?username=")
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
