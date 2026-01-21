from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarTest(TestCase):
    def setUp(self) -> None:
        self.driver1 = get_user_model().objects.create_user(
            username="panjaby",
            password="lkj456_&^%",
            first_name="Radj",
            last_name="Mallah",
            license_number="OIU78543"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="speedster",
            password="fast&furious99",
            first_name="Vin",
            last_name="Diesel",
            license_number="SPD12345"
        )

        self.driver3 = get_user_model().objects.create_user(
            username="driftking",
            password="tokyoDrift!",
            first_name="Takashi",
            last_name="Fujimoto",
            license_number="DK67890"
        )

        self.client.force_login(self.driver1)
        self.client.force_login(self.driver2)
        self.client.force_login(self.driver3)

        self.man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.man2 = Manufacturer.objects.create(name="Tesla", country="USA")
        self.man3 = Manufacturer.objects.create(
            name="Tata Motors", country="India"
        )

        self.car1 = Car.objects.create(
            model="Novus",
            manufacturer=self.man3,
        )
        self.car2 = Car.objects.create(
            model="Model Y",
            manufacturer=self.man2,
        )
        self.car1.drivers.add(self.driver1)
        self.car2.drivers.add(self.driver2, self.driver3)

    def test_car_list_without_searching(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "Yaris")
        self.assertContains(response, "Novus")
        self.assertContains(response, "Model Y")

    def test_search(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "O"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Novus")
        self.assertContains(response, "Model Y")

    def test_cat_detail_page(self):
        res = self.client.get(
            reverse(
                "taxi:car-detail",
                args=[self.car2.id]
            )
        )
        self.assertEqual(res.status_code, 200)
