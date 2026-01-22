from django.test import TestCase
from django.urls import reverse

from taxi.models import Car

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
