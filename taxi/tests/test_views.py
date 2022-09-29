from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.views import index

INDEX_URL = reverse("taxi:index")


class PublicIndexTests(TestCase):

    def test_login_required_index_url(self):
        response = self.client.get(INDEX_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_login_required_assign_driver_button(self):
        self.manufacturer = Manufacturer.objects.create(name="test1", country="UA")
        self.car = Car.objects.create(model="test_1", manufacturer_id=1)
        response = self.client.get(
            reverse("taxi:toggle-car-assign",
                    kwargs={"pk": self.car.pk}))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password1",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("taxi/index.html")

    def test_assign_user_to_car(self):
        self.manufacturer = Manufacturer.objects.create(name="test_manu", country="UK")
        self.driver = get_user_model().objects.create_user(
            username="test_user1",
            password="password11",
            license_number="WSD12345")
        car_without_user = Car.objects.create(model="test_car", manufacturer_id=self.manufacturer.pk)
        car_with_user = Car.objects.create(model="test_car1", manufacturer_id=self.manufacturer.pk)
        car_with_user.drivers.add(self.user, self.driver)
        car_without_user.drivers.add(self.driver)
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": car_with_user.pk}))
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": car_without_user.pk}))

        self.assertEqual(list(car_with_user.drivers.all()), list([self.driver]))
        self.assertEqual(list(car_without_user.drivers.all()), list([self.user, self.driver]))
