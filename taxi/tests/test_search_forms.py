from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestSearchingFeature(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD>",
            license_number="QWE12345"
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="mykola",
            password="<PASSWORD>",
            license_number="YWE12349"
        )
        for driver in range(6):
            get_user_model().objects.create_user(
                username=f"testuser{driver}",
                password="<PASSWORD>",
                license_number=f"TWE1234{driver}"
            )

        Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        for manufacturer in range(6):
            Manufacturer.objects.create(
                name=f"BMW{manufacturer}",
                country="Germany"
            )

        Car.objects.create(
            model="E250",
            manufacturer=Manufacturer.objects.get(name="Mercedes"),
        )
        for car in range(6):
            Car.objects.create(
                model=f"X{car}",
                manufacturer=Manufacturer.objects.get(name="BMW1"),
            )

    def test_driver_username_search(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "testuser"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser0")
        self.assertNotContains(response, "mykola")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "testuser", "page": 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser5")

    def test_car_model_search(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X0")
        self.assertNotContains(response, "E250")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X", "page": 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")

    def test_manufacturer_name_search(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW0")
        self.assertNotContains(response, "Mercedes")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"model": "BMW", "page": 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW5")
