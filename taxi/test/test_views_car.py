from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateCarrTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_name_1", country="US"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_name_1",
            password="password123",
            license_number="AAA33033",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="test_model_search",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)
        self.car_list_url = reverse("taxi:car-list")
        self.car_create_url = reverse("taxi:car-create")

    def test_retrieve_car(self):
        response = self.client.get(self.car_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        cars = Car.objects.all()

        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_list(self):
        form_data = {"model": "test_model_search"}
        response = self.client.get(self.car_list_url, data=form_data)
        cars = Car.objects.all().filter(model=form_data["model"])

        self.assertEqual(len(response.context["car_list"]), len(cars))
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("car", response.context)
        self.assertEqual(response.context["car"], self.car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_create_car(self):
        form_data = {
            "model": "new_model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        self.assertFalse(Car.objects.filter(model=form_data["model"]).exists())
        response = self.client.post(self.car_create_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model=form_data["model"]).exists())

        new_car = Car.objects.get(model=form_data["model"])
        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.id, form_data["manufacturer"])
        self.assertEqual(new_car.drivers.all()[0].id, form_data["drivers"][0])

    def test_update_car(self):
        form_data = {
            "model": "test_update_model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        url = reverse("taxi:car-update", kwargs={"pk": self.car.id})
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, form_data["model"])
        self.assertEqual(self.car.manufacturer.id, form_data["manufacturer"])
        self.assertEqual(self.car.drivers.all()[0].id, form_data["drivers"][0])

    def test_delete_car(self):
        count = Car.objects.count()
        url = reverse("taxi:car-delete", kwargs={"pk": self.car.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count() + 1, count)

    def test_toggle_car_assign(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})
        count_start = self.car.drivers.count()
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(self.car.drivers.count(), count_start + 1)
        self.client.post(url)
        self.assertEqual(self.car.drivers.count(), count_start)
