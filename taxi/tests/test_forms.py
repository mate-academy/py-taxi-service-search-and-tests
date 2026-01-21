from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car


class CarSearchFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="Test"
        )
        self.car1 = Car.objects.create(
            model="Test1", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Test2", manufacturer=self.manufacturer
        )

    def test_search_form_display(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertEqual(response.status_code, 200)
