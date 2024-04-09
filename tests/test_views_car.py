from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicFormatTest(TestCase):

    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.car1 = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test Car1"
        )
        self.car2 = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test Car2"
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_create_car(self):
        driver = get_user_model().objects.create(
            username="Test User",
            first_name="Test Name",
            last_name="Test Last Name",
            license_number="TES12345",
        )
        form_data = {
            "model": "Test car model",
            "manufacturer": self.manufacturer.pk,
            "drivers": driver.pk
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)
        car = Car.objects.get(model=form_data["model"])
        self.assertEqual(car.model, form_data["model"])
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertRedirects(response, "/cars/")

    def test_query_search_filter_by_part_of_model(self):
        driver1 = get_user_model().objects.create(
            username="Test User1",
            first_name="Test Name1",
            last_name="Test Last Name1",
            license_number="TES12345",
        )
        driver2 = get_user_model().objects.create(
            username="Test User2",
            first_name="Test Name2",
            last_name="Test Last Name2",
            license_number="TEQ12345",
        )
        self.car1.drivers.set([driver1])
        self.car2.drivers.set([driver2])

        response = self.client.get("/cars/", {"model": "tes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            [self.car1, self.car2]
        )

    def test_search_with_empty_query(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["object_list"]),
            Car.objects.count()
        )

    def test_search_with_invalid_data(self):
        response = self.client.get("/cars/", {"model": "model"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)
