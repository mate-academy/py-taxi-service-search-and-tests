from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CARS_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required_list_page(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "qwerty12"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars_list(self):
        self.brand = Manufacturer.objects.create(name="Test", country="Test")
        Car.objects.create(model="Test1", manufacturer=self.brand)
        Car.objects.create(model="Test2", manufacturer=self.brand)

        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "qwerty12"
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        data = "Test234"
        self.client.post(
            reverse("taxi:manufacturer-create"),
            data={"name": data, "country": data}
        )

        new_manufacturer = Manufacturer.objects.get(name=data)

        self.assertEqual(new_manufacturer.name, data)
        self.assertEqual(new_manufacturer.country, data)

    def test_manufacturer_search(self):
        response = self.client.get("/manufacturers/?name=es")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="es")
        )
