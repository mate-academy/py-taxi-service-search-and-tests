from django.urls import reverse
from taxi.models import Car, Manufacturer
from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class PublicCarTest(TestCase):
    CAR_URL = reverse("taxi:car-list")

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(self.CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    CAR_URL = reverse("taxi:car-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="bogdanchik",
            password="bbb1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        driver = get_user_model().objects.create(
            username="driver",
            password="bog1234",
            first_name="Bohdan",
            last_name="Bielyi",
            license_number="BBB11111",
        )
        car_1 = Car.objects.create(
            model="HR-V",
            manufacturer=manufacturer,
        )
        car_1.drivers.add(driver)
        car_2 = Car.objects.create(
            model="Pilot",
            manufacturer=manufacturer,
        )
        car_2.drivers.add(driver)

        response = self.client.get(self.CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            response.context["car_list"],
            list(cars)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        driver = get_user_model().objects.create(
            username="driver",
            password="bog1234",
            first_name="Bohdan",
            last_name="Bielyi",
            license_number="BBB11111",
        )
        car_1 = Car.objects.create(
            model="HR-V",
            manufacturer=manufacturer,
        )
        car_1.drivers.add(driver)
        car_2 = Car.objects.create(
            model="Pilot",
            manufacturer=manufacturer,
        )
        car_2.drivers.add(driver)
        response = self.client.get(self.CAR_URL, {"model": "Pilot"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pilot")
        self.assertNotContains(response, "HR-V")
