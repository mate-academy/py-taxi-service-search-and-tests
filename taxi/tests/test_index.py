from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class IndexViewTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="dispatcher",
            password="testpass123",
            license_number="AAA12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(model="Prius", manufacturer=manufacturer)
        self.client.force_login(self.driver)

    def test_index_displays_object_counts_and_visit_counter(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)
