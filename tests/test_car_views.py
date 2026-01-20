from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse

from taxi.models import Driver, Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)

    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(
            reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_update_login_required(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[self.car.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[self.car.id]))
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(model="Mottorolla",
                                       manufacturer=self.manufacturer)
        self.car3 = Car.objects.create(model="Shocoborolla",
                                       manufacturer=self.manufacturer)
        self.cars = Car.objects.all()

    def test_retrieve_cars_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(self.cars))

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Mottorolla")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mottorolla")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Shocoborolla")

    def test_car_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=nonexistent")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context["car_list"]),
                            list(self.cars))
