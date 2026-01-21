from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL: str = reverse("taxi:car-list")


class PublicCarListViewTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PrivateCarListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="TestPassword123",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        driver = get_user_model().objects.create(
            username="test_driver",
            password="TestDriver123",
            first_name="Test",
            last_name="Driver",
            license_number="TEST12345"
        )

        car1 = Car.objects.create(
            model="Jetta",
            manufacturer=manufacturer
        )
        car2 = Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer
        )

        car1.drivers.add(driver)
        car2.drivers.add(driver)

        response = self.client.get(CAR_LIST_URL)

        cars_from_db = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars_from_db)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_cars_by_model(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        car1 = Car.objects.create(
            model="Jetta",
            manufacturer=manufacturer
        )
        car2 = Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_LIST_URL, {"model": "Mustang"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(car2, response.context["car_list"])
        self.assertNotIn(car1, response.context["car_list"])
