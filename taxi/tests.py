from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="mainuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_driver_search_by_username(self):
        Driver.objects.create_user(
            username="alice",
            password="pass12345",
            license_number="AAA11111",
        )
        Driver.objects.create_user(
            username="bob",
            password="pass12345",
            license_number="BBB22222",
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "ali"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

        object_list = response.context["object_list"]
        usernames = [d.username for d in object_list]

        self.assertIn("alice", usernames)
        self.assertNotIn("bob", usernames)

    def test_car_search_by_model(self):
        m = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer=m)
        Car.objects.create(model="Corolla", manufacturer=m)

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "model"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

        object_list = response.context["object_list"]
        models = [c.model for c in object_list]

        self.assertIn("Model S", models)
        self.assertNotIn("Corolla", models)

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "toy"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

        object_list = response.context["object_list"]
        names = [m.name for m in object_list]

        self.assertIn("Toyota", names)
        self.assertNotIn("Tesla", names)


class CoreFeatureTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="user1",
            password="testpass123",
            license_number="CCC33333",
        )
        self.client.force_login(self.driver)

    def test_index_increments_num_visits(self):
        url = reverse("taxi:index")

        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.context["num_visits"], 1)

        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.context["num_visits"], 2)

    def test_toggle_assign_to_car_adds_and_removes_driver(self):
        m = Manufacturer.objects.create(name="BMW", country="Germany")
        car = Car.objects.create(model="X5", manufacturer=m)

        toggle_url = reverse("taxi:toggle-car-assign", args=[car.id])

        self.client.get(toggle_url)
        self.driver.refresh_from_db()
        self.assertIn(car, self.driver.cars.all())

        self.client.get(toggle_url)
        self.driver.refresh_from_db()
        self.assertNotIn(car, self.driver.cars.all())
