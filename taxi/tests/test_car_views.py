from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicTestCarViews(TestCase):
    def test_car_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test_password",
        )
        self.client.force_login(self.user)
        manufacturer_1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        Car.objects.create(model="Toyota Camry", manufacturer=manufacturer_1)
        Car.objects.create(model="Toyota Prado", manufacturer=manufacturer_1)
        Car.objects.create(model="Audi A4", manufacturer=manufacturer_2)
        Car.objects.create(model="Audi S4", manufacturer=manufacturer_2)

    def test_car_retrieve_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(cars),
            list(response.context["car_list"])
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_form_in_car(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Audi"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi A4")
        self.assertContains(response, "Audi S4")
        self.assertNotContains(response, "Toyota Camry")
        self.assertNotContains(response, "Toyota Prado")
