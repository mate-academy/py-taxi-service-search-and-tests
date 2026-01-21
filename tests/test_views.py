from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer

URL_MANUFACTURER_LIST = "taxi:manufacturer-list"
URL_CAR_LIST = "taxi:car-list"


class TaxiViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="interjkee",
            password="1234",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_car_list_search(self):
        response = self.client.get(reverse(URL_CAR_LIST) + "?model=Camry")

        if response.context:
            self.assertIn("car_list", response.context)
            car = Car.objects.filter(model="Camry")
            self.assertEqual(
                list(response.context["car_list"]),
                list(car)
            )

    def test_car_list_search_nonexisting_value(self):
        response = (
            self.client.get(reverse(URL_CAR_LIST) + "?model=nonexistent")
        )

        if response.context:
            self.assertIn("car_list", response.context)
            self.assertEqual(
                list(response.context["car_list"]),
                []
            )

    def test_manufacturer_list_authenticated_user(self):
        self.client.login(username="interjkee", password="1234")
        response = self.client.get(reverse(URL_MANUFACTURER_LIST))

        if response.context:
            self.assertIn("manufacturer_list", response.context)
            manufacturer = Manufacturer.objects.all()
            self.assertEqual(
                list(response.context["manufacturer_list"]),
                list(manufacturer)
            )

    def test_manufacturer_list_unauthenticated_user(self):
        response = self.client.get(reverse(URL_MANUFACTURER_LIST))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse(URL_MANUFACTURER_LIST)}"
        )

    def test_assign_to_car_authenticated_user(self):
        self.client.login(username="interjkee", password="1234")
        url = reverse("taxi:toggle-car-assign", args=[self.car1.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_assign_to_car_unauthenticated_user(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car1.id])

        response = self.client.post(url)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={url}"
        )
