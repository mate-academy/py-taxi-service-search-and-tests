from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewsTest(TestCase):
    def test_login_required(self):
        for url in (INDEX_URL, MANUFACTURER_LIST_URL, CAR_LIST_URL):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

    def test_index_counts_and_visits(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)

        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_visits"], 2)

    def test_list_uses_template_and_search_form(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn("search_form", response.context)

    def test_search_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(MANUFACTURER_LIST_URL, {"title": "toy"})

        self.assertEqual(
            list(response.context["manufacturer_list"]), [self.manufacturer]
        )

    def test_search_by_model(self):
        camry = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)

        response = self.client.get(CAR_LIST_URL, {"title": "cam"})
        self.assertEqual(list(response.context["car_list"]), [camry])

    def test_search_by_username(self):
        get_user_model().objects.create_user(
            username="john", password="test12345", license_number="JHN12345"
        )

        response = self.client.get(DRIVER_LIST_URL, {"title": "jo"})
        self.assertEqual(
            [driver.username for driver in response.context["driver_list"]],
            ["john"],
        )
