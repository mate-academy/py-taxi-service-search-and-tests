from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.views import CarListView

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            license_number="TES12345"
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_retrieve_cars(self):
        Car.objects.create(
            model="test_model1",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="test_model2",
            manufacturer=self.manufacturer
        )
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_create_car(self):
        car_data = {
            "model": "test_model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk]
        }
        res = self.client.post(reverse("taxi:car-create"), car_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Car.objects.count(), 1)
        self.assertRedirects(res, "/cars/")

    def test_update_car(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        car.drivers.set([self.user])
        car_update = {
            "model": "test_model_update",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk]
        }
        res = self.client.post(
            reverse("taxi:car-update", args=[car.pk]),
            car_update
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cars/")
        car.refresh_from_db()
        self.assertEqual(car.model, "test_model_update")
        self.assertEqual(car.manufacturer.pk, self.manufacturer.pk)

    def test_delete_car(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        car.drivers.set([self.user])
        res = self.client.post(reverse("taxi:car-delete", args=[car.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Car.objects.count(), 0)
        self.assertRedirects(res, "/cars/")

    def test_get_context_data_car(self):
        car1 = Car.objects.create(
            model="test_model1",
            manufacturer=self.manufacturer,
        )
        car2 = Car.objects.create(
            model="test_model2",
            manufacturer=self.manufacturer,
        )
        car1.drivers.set([self.user])
        car2.drivers.set([self.user])
        request = self.factory.get(
            reverse("taxi:car-list"),
            {"model": "Test_model2"}
        )
        request.user = self.user

        view = CarListView()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().model, "test_model2")
