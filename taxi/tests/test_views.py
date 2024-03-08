from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicAccessTest(TestCase):
    def test_login_required(self) -> None:
        result_index = self.client.get(INDEX_URL)
        result_manufacturer = self.client.get(MANUFACTURER_LIST_URL)
        result_car = self.client.get(CAR_LIST_URL)
        result_driver = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(result_index.status_code, 200)
        self.assertNotEqual(result_manufacturer.status_code, 200)
        self.assertNotEqual(result_car.status_code, 200)
        self.assertNotEqual(result_driver.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="BMW M5 F90", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_driver(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
