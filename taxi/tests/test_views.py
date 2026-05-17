from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class PublicTaxiTest(TestCase):
    def test_login_required_for_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="testuser",
            password="test12345",
            license_number="ABC12345"
        )

        cls.manufacturer_1 = Manufacturer.objects.create(
            name="BMW Group",
            country="Germany"
        )
        cls.manufacturer_2 = Manufacturer.objects.create(
            name="Toyota Motor",
            country="Japan"
        )

        cls.car_1 = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer_1
        )
        cls.car_2 = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer_2
        )

        cls.driver_1 = Driver.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="AAA11111"
        )
        cls.driver_2 = Driver.objects.create_user(
            username="mike_taxi",
            password="test12345",
            license_number="BBB22222"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_list_view_url_exists(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "mike_taxi")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertNotContains(response, "Corolla")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW Group")
        self.assertNotContains(response, "Toyota Motor")

    def test_toggle_assign_to_car_add(self):
        self.assertNotIn(self.car_1, self.user.cars.all())

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car_1.id])
        )
        self.user.refresh_from_db()

        self.assertIn(self.car_1, self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car_1)
        self.assertIn(self.car_1, self.user.cars.all())

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car_1.id])
        )
        self.user.refresh_from_db()

        self.assertNotIn(self.car_1, self.user.cars.all())
