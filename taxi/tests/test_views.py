from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class IndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for id_ in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"Brand {id_}",
                country="Ukraine"
            )

            Driver.objects.create_user(
                username=f"driver {id_}",
                license_number=str(id_)
            )

            Car.objects.create(
                model=f"Model {id_}",
                manufacturer=manufacturer
            )

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="user1",
            password="top_user",
        )
        self.client.force_login(self.user)

    def test_index_counters(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_cars"], 10)
        self.assertEqual(response.context["num_drivers"], 11)
        self.assertEqual(response.context["num_manufacturers"], 10)


class ManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for id_ in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"Brand {id_}",
                country="Ukraine"
            )

            Driver.objects.create_user(
                username=f"driver {id_}",
                license_number=str(id_)
            )

            Car.objects.create(
                model=f"Model {id_}",
                manufacturer=manufacturer
            )

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="user1",
            password="top_user",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_correct_status(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_pagination(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.context["manufacturer_list"].count(), 5)

    def test_manufacturer_update(self):
        self.manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
            {"name": "BMW", "country": "Germany"}
        )
        self.assertEqual(response.status_code, 302)

        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "BMW")


class CarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="top_user",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

    def test_car_creation(self):
        self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "M5",
                "drivers": self.user.id,
                "manufacturer": self.manufacturer.id
            }
        )
        self.assertEqual(Car.objects.last().model, "M5")

    def test_car_detail(self):
        self.car = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertContains(response, "M5")

    def test_car_delete(self):
        self.car = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer
        )

        response = self.client.delete(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.last(), None)
