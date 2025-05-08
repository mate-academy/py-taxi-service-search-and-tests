from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_VIEW_URL = reverse("taxi:car-list")
CAR_CREATE_VIEW_URL = reverse("taxi:car-create")


class PublicCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_car_list_view_login_required(self):
        response = self.client.get(CAR_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_view_login_required(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_view_login_required(self):
        response = self.client.get(CAR_CREATE_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_view_login_required(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_view_login_required(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="First Car",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Second Car",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Third Car",
            manufacturer=self.manufacturer
        )

    def test_car_list_view_without_search(self):
        cars = Car.objects.all()
        response = self.client.get(CAR_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertContains(response, "First Car")
        self.assertContains(response, "Second Car")
        self.assertContains(response, "Third Car")

    def test_car_list_view_with_search(self):
        cars = Car.objects.all()
        response = self.client.get(CAR_LIST_VIEW_URL, {"model": "fir"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertContains(response, "First Car")
        self.assertNotContains(response, "Second Car")
        self.assertNotContains(response, "Third Car")

    def test_car_detail_view(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_car_create_view(self):
        car_data = {
            "model": "Test car2",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        response_get = self.client.get(CAR_CREATE_VIEW_URL)
        self.client.post(CAR_CREATE_VIEW_URL, data=car_data)
        new_car = Car.objects.get(model=car_data["model"])
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/car_form.html")
        self.assertEqual(new_car.model, car_data["model"])
        self.assertEqual(
            new_car.manufacturer,
            Manufacturer.objects.get(id=car_data["manufacturer"])
        )
        self.assertEqual(new_car.drivers.count(), 1)

    def test_car_update_view(self):
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Test Country2"
        )
        self.new_driver = get_user_model().objects.create_user(
            username="new_driver",
            password="test123",
            license_number="AMD91911"
        )
        car_update_data = {
            "model": "Updated model",
            "manufacturer": self.manufacturer2.id,
            "drivers": [self.new_driver.id]
        }
        url = reverse("taxi:car-update", args=[self.car.id])
        response_get = self.client.get(url)
        self.client.post(url, data=car_update_data)
        updated_car = Car.objects.get(id=self.car.id)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/car_form.html")
        self.assertEqual(updated_car.model, car_update_data["model"])
        self.assertEqual(
            updated_car.manufacturer,
            Manufacturer.objects.get(id=car_update_data["manufacturer"])
        )
        self.assertEqual(updated_car.drivers.count(), 1)

    def test_car_delete_view(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        response_get = self.client.get(url)
        self.client.post(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/car_confirm_delete.html")
        self.assertEqual(Car.objects.count(), 2)
