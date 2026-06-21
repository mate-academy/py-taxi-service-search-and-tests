from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TaxiViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="AlexKing",
            password="qwerty",
            first_name="Alex",
            last_name="Smith",
            license_number="KMZS12345",
        )
        self.client.force_login(self.driver)

        self.manufacturer = (Manufacturer.objects.create
                             (name="BMW", country="Germany"))
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer,
        )

    def test_login_required_redirect(self):
        self.client.logout()
        url = reverse("taxi:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_index_count(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_visits"], 1)

        response2 = self.client.get(reverse("taxi:index"))
        self.assertEqual(response2.context["num_visits"], 2)

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.assertNotIn(self.driver, self.car.drivers.all())

        response = self.client.get(url)
        self.assertRedirects(response,
                             reverse("taxi:car-detail", args=[self.car.id]))

        self.assertIn(self.driver, self.car.drivers.all())
        self.client.get(url)
        self.assertNotIn(self.driver, self.car.drivers.all())

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(name="ZAZ", country="Ukraine")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, data={"name": "b"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(response.context["manufacturer_list"][0].name, "BMW")

    def test_car_list_search(self):
        Car.objects.create(model="M3", manufacturer=self.manufacturer)
        url = reverse("taxi:car-list")
        response = self.client.get(url, data={"model": "x"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "X5")

    def test_driver_list_search(self):
        get_user_model().objects.create_user(
            username="Dima",
            password="qw32rerty",
            first_name="Dmitro",
            last_name="Shevchenko",
            license_number="KMZA12346",
        )
        url = reverse("taxi:driver-list")
        response = self.client.get(url, data={"username": "Alex"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(response.context["driver_list"][0].username,
                         "AlexKing")
