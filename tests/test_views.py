from django.test import TestCase, Client

from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Car


class SearchTest(TestCase):
    def test_search_manufacturer(self):
        client = Client()
        response = client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], ManufacturerSearchForm)

    def test_search_car_filtering(self):
        Car.objects.create(name="BMW", country="Germany")
        Car.objects.create(name="Ferrari", country="Italy")

        client = Client()
        response = client.get(reverse("taxi:car-list"), {"name": "BMW"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Ferrari")
