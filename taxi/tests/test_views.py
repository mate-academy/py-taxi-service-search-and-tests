from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class PublicViewsTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/",
        )


class PrivateViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="admin",
            password="test12345",
            license_number="ABC12345",
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_context(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

    def test_num_visits_increment(self):
        self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_visits"], 2)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html",
        )
        self.assertContains(response, "BMW")

    def test_car_list_view(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")

    def test_driver_list_view(self):
        Driver.objects.create_user(
            username="alex",
            password="test12345",
            license_number="XYZ54321",
        )

        response = self.client.get(
            reverse("taxi:driver-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alex")

    def test_car_detail_view(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-detail", args=[car.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )

        self.assertNotIn(car, self.driver.cars.all())

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[car.pk])
        )

        self.driver.refresh_from_db()
        self.assertIn(car, self.driver.cars.all())

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[car.pk])
        )

        self.driver.refresh_from_db()
        self.assertNotIn(car, self.driver.cars.all())
