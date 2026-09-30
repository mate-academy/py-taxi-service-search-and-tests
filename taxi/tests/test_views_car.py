from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.tests.base import LoggedInTestCase

CAR_LIST_URL = reverse("taxi:car-list")


class PrivateCarViewsTest(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

    def test_list_pagination_and_search(self):
        for model in [
            "Corolla",
            "Camry",
            "Yaris",
            "Supra",
            "Prius",
            "Corvette",
            "Civic",
        ]:
            Car.objects.create(model=model, manufacturer=self.manufacturer)

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertEqual(response.context["paginator"].count, 7)

        response = self.client.get(CAR_LIST_URL, {"searched_value": "cor"})
        self.assertEqual(
            response.context["paginator"].count, 2
        )  # Corolla, Corvette
        self.assertEqual(
            response.context["search_form"].initial["searched_value"], "cor"
        )

    def test_create_car(self):
        driver = get_user_model().objects.create_user(
            username="driver1", password="test12345", license_number="XYZ98765"
        )
        data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.pk,
            "drivers": [driver.pk],
        }
        response = self.client.post(reverse("taxi:car-create"), data)

        self.assertRedirects(response, CAR_LIST_URL)
        car = Car.objects.get(model="Corolla")
        self.assertEqual(list(car.drivers.all()), [driver])

    def test_delete_car(self):
        car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        response = self.client.post(reverse("taxi:car-delete", args=[car.pk]))

        self.assertRedirects(response, CAR_LIST_URL)
        self.assertFalse(Car.objects.exists())
