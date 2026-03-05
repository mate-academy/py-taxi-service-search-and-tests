from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer
from taxi.views import CarListView


class CarListTest(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("taxi:car-list"))

    def test_get_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(CarListView.paginate_by, 5)

    def test_get_context(self):
        self.assertIn("search", self.response.context)

    def test_search(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="test")
        for i in range(10):
            Car.objects.create(
                model=f"test_model_{i}",
                manufacturer=manufacturer,
            )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "test_model_1"}
        )
        cars = response.context.get("car_list")

        self.assertEqual(len(cars), 1)
        self.assertTrue(isinstance(cars[0], Car))
