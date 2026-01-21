from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ListViewsAuthTests(TestCase):
    def test_list_views_require_login(self):
        for name in [
            "taxi:driver-list",
            "taxi:car-list",
            "taxi:manufacturer-list"
        ]:
            with self.subTest(name=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 302)
                self.assertIn("/login", resp.url)


class ListViewsRenderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u1",
            password="p1",
            license_number="LIC00001"
        )
        m1 = Manufacturer.objects.create(name="BMW", country="Germany")
        m2 = Manufacturer.objects.create(name="Toyota", country="Japan")
        cls.c1 = Car.objects.create(model="X5", manufacturer=m1)
        cls.c2 = Car.objects.create(model="Corolla", manufacturer=m2)
        cls.c1.drivers.add(cls.user)

    def setUp(self):
        self.client.login(username="u1", password="p1")


class ToggleAssignTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u2",
            password="p2",
            license_number="LIC00002"
        )
        cls.m = Manufacturer.objects.create(name="VW", country="Germany")
        cls.car = Car.objects.create(model="Golf", manufacturer=cls.m)

    def setUp(self):
        self.client.login(username="u2", password="p2")

    def test_toggle_assign_to_car_adds_and_removes(self):
        # add
        resp1 = self.client.post(
            reverse("taxi:toggle-car-assign",
                    args=[self.car.pk])
        )
        self.assertEqual(resp1.status_code, 302)
        self.assertTrue(Driver.objects.get(pk=self.user.pk)
                        .cars.filter(pk=self.car.pk).exists())
        # remove
        resp2 = self.client.post(
            reverse("taxi:toggle-car-assign",
                    args=[self.car.pk])
        )
        self.assertEqual(resp2.status_code, 302)
        self.assertFalse(Driver.objects.
                         get(pk=self.user.pk).cars.
                         filter(pk=self.car.pk).exists()
                         )


class SearchViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver1 = Driver.objects.create_user(
            username="alice",
            password="p",
            license_number="ALICE001"
        )
        cls.driver2 = Driver.objects.create_user(
            username="BobBuilder",
            password="p",
            license_number="BOB00001"
        )
        cls.m1 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        cls.m2 = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        cls.c1 = Car.objects.create(
            model="Model S",
            manufacturer=cls.m1
        )
        cls.c2 = Car.objects.create(
            model="E-Class",
            manufacturer=cls.m2
        )

    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url, {"username": "bob"})
        self.assertEqual(resp.status_code, 200)

        drivers = list(resp.context["driver_list"])
        self.assertEqual(drivers, [self.driver2])
        self.assertContains(resp, self.driver2.username)

    def test_car_search_by_model(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"model": "model"})
        self.assertEqual(resp.status_code, 200)

        cars = list(resp.context["car_list"])
        self.assertEqual(cars, [self.c1])
        self.assertContains(resp, self.c1.model)

    def test_manufacturer_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        resp = self.client.get(url, {"name": "merc"})
        self.assertEqual(resp.status_code, 200)

        manufacturers = list(resp.context["manufacturer_list"])
        self.assertEqual(manufacturers, [self.m2])
        self.assertContains(resp, self.m2.name)

    def test_empty_query_returns_all(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        cars = list(resp.context["car_list"])
        self.assertEqual(set(cars), {self.c1, self.c2})

    def setUp(self):
        self.client.login(username="alice", password="p")
