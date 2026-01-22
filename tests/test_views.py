from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

URL_MANUFACTURER_LIST = "taxi:manufacturer-list"

URL_CAR_LIST = "taxi:car-list"


class TestCarListSearchView(TestCase):
    def test_car_list_search(self) -> None:
        response = self.client.get(reverse(URL_CAR_LIST) + "?model=1")

        if response.context:
            self.assertIn("car_list", response.context)
            car = Car.objects.filter(model="test car 1")
            self.assertEqual(
                list(response.context["car_list"]),
                list(car)
            )

    def test_car_list_search_nonexisting_value(self) -> None:
        response = self.client.get(
            reverse(URL_CAR_LIST) + "?model=nonexistent")

        if response.context:
            self.assertIn("car_list", response.context)
            self.assertEqual(
                list(response.context["car_list"]),
                []
            )


class PublicManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="krixn",
            password="1337",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW")

    def test_manufacturer_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:manufacturer-list')}"
        )

    def test_toggle_assign_to_car_view_authenticated_user(self):
        self.client.login(username="krixn", password="1337")

        car = Car.objects.create(model="Bazuka",
                                 manufacturer=self.manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_toggle_assign_to_car_view_unauthenticated_user(self):
        car = Car.objects.create(model="Bazuka",
                                 manufacturer=self.manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.id])

        response = self.client.post(url)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={url}"
        )
