from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testcar",
            password="car123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="KIA",
            country="Korea"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(
            model="KIA Soul",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="KIA Sorento",
            manufacturer=self.manufacturer
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_create_car(self):
        driver = Driver.objects.create(
            username="user",
            license_number="ABC55555",
            first_name="Ban",
            last_name="User",
            password="user123"
        )
        form_data = {
            "model": "KIA Sportage",
            "manufacturer": self.manufacturer.id,
            "drivers": [driver.id, ]
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])
        self.assertEqual(
            list(new_car.drivers.values_list("id", flat=True)),
            form_data["drivers"]
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="KIA Soul",
            manufacturer=self.manufacturer
        )
        form_data = {
            "drivers": []
        }
        self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            data=form_data
        )
        car.refresh_from_db()
        self.assertEqual(
            list(car.drivers.values_list("id", flat=True)),
            form_data["drivers"]
        )
