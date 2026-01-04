from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class LoginRequiredViewsTests(TestCase):
    def test_login_required_redirects(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)


class IndexViewTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver",
            password="pass12345",
            license_number="ABC12345"
        )
        self.client.login(username="driver", password="pass12345")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

    def test_index_view_template_used(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertTemplateUsed(response, "taxi/index.html")


class ToggleAssignToCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

        self.driver = Driver.objects.create_user(
            username="driver",
            password="pass12345",
            license_number="ABC12345"
        )

        self.client.login(username="driver", password="pass12345")

    def test_assign_car_to_driver(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.client.get(url)

        self.assertIn(self.car, self.driver.cars.all())

    def test_unassign_car_from_driver(self):
        self.driver.cars.add(self.car)

        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.client.get(url)

        self.assertNotIn(self.car, self.driver.cars.all())
