from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Volkswagen AG")
        Manufacturer.objects.create(name="Mercedes Benz AG")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEquals(res.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Volkswagen AG")
        searched_name = "Volkswagen AG"
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": searched_name}
        )
        self.assertEqual(response.status_code, 200)
        manufacturer_in_context = Manufacturer.objects.filter(
            name__icontains=searched_name
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], manufacturer_in_context
        )


class PublicCarTest(TestCase):

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user2",
            password="testpass",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search_by_name(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Ford Motor Co")
        Car.objects.create(
            model="Ford", manufacturer=manufacturer
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"model": "Ford", "manufacturer": "Ford Motor Co"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Ford",
            count=1,
            status_code=200
        )
        self.assertContains(
            response,
            "Ford Motor Co",
            count=1,
            status_code=200
        )
