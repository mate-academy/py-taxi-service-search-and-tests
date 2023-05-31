from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            country="Country 1"
        )
        self.car = Car.objects.create(
            model="Car Model",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="test_password12345",
            license_number="ABC12345"
        )

    def test_index_view(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_manufacturer_list_view(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_list_view(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_list_view(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_toggle_assign_to_car_view(self) -> None:
        self.client.force_login(self.driver)

        response = self.client.get(
            reverse("taxi:toggle-car-assign",
                    args=[self.car.pk]
                    )
        )
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Exception) as response:
            self.client.get(reverse("taxi:toggle-car-assign", args=[999]))

        self.assertTrue("does not exist" in str(response.exception))

    def test_car_detail_view(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_driver_detail_view(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
