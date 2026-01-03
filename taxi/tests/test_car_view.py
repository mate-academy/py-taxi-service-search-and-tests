from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test username",
            password="Pass1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        car1 = Car.objects.create(
            manufacturer=manufacturer,
            model="model name 1",
        )
        car1.drivers.add(self.driver)
        car1.save()
        car2 = Car.objects.create(
            manufacturer=manufacturer,
            model="model name 2",
        )
        car2.drivers.add(self.driver)
        car2.save()
        car2 = Car.objects.create(
            manufacturer=manufacturer,
            model="another name",
        )
        car2.drivers.add(self.driver)
        car2.save()

    def test_retrieve_all_cars(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_car(self):
        res = self.client.get(CAR_LIST_URL, {"model": "model"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "model name 1")
        self.assertContains(res, "model name 2")
        self.assertNotContains(res, "another name")


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.url = reverse("taxi:toggle-car-assign", args=[self.car.pk])

    def test_assign_car_to_driver(self):
        self.assertNotIn(self.car, self.driver.cars.all())

        response = self.client.post(self.url)

        self.driver.refresh_from_db()

        self.assertIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.pk])
        )

    def test_remove_car_from_driver(self):
        self.driver.cars.add(self.car)
        self.driver.save()

        self.assertIn(self.car, self.driver.cars.all())

        response = self.client.post(self.url)

        self.driver.refresh_from_db()

        self.assertNotIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.pk])
        )
