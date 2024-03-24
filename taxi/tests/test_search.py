from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class TestSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test123"
        )
        self.client.force_login(self.user)

        driver_data = {
            "Atest": "ADC12345",
            "atest": "ABC12534",
            "btest": "ABC51234"
        }
        for some_name, license_number in driver_data.items():
            Driver.objects.create(
                username=some_name,
                password=license_number,
                license_number=license_number
            )
            Manufacturer.objects.create(
                name=some_name,
                country="Anywhere"
            )
            Car.objects.create(
                model=some_name,
                manufacturer=Manufacturer.objects.get(id=1)
            )

    def test_search_drivers_check_values(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "a"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Atest")
        self.assertContains(response, "atest")
        self.assertNotContains(response, "btest")

    def test_search_drivers_check_len(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "a"}
        )
        self.assertEqual(
            len(response.context_data["object_list"]),
            len(Driver.objects.filter(username__icontains="A"))
        )

    def test_search_cars_check_values(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "a"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Atest")
        self.assertContains(response, "atest")
        self.assertNotContains(response, "btest")

    def test_search_car_check_len(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "a"}
        )
        self.assertEqual(
            len(response.context_data["object_list"]),
            len(Car.objects.filter(model__icontains="A"))
        )

    def test_search_manufacturer_check_values(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "a"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Atest")
        self.assertContains(response, "atest")
        self.assertNotContains(response, "btest")

    def test_search_manufacturer_check_len(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "a"}
        )
        self.assertEqual(
            len(response.context_data["object_list"]),
            len(Manufacturer.objects.filter(name__icontains="A"))
        )
