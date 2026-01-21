from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateHomeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_visit_counter(self):
        visits = 3

        for visit in range(visits):
            response = self.client.get(reverse("taxi:index"))
            self.assertEqual(response.context["num_visits"], visit + 1)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        Manufacturer.objects.create(name="abc", country="US")
        Manufacturer.objects.create(name="cba", country="UK")
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(
                manufacturers[
                    0 : len(list(response.context["manufacturer_list"]))
                ]
            ),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create",
            ),
            {"name": "Lincoln", "country": "USA"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.get(id=1).name, "Lincoln")

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}
            ),
            {"name": "Not Lincoln", "country": "USA"},
        )
        Manufacturer.objects.get(id=manufacturer.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=manufacturer.id).name, "Not Lincoln"
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )

    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars[0 : len(list(response.context["car_list"]))]),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        Car.objects.create(model="testmodel", manufacturer=self.manufacturer)
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, "Continental"
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": "Not Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Not Continental")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers[0 : len(list(response.context["driver_list"]))]),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
