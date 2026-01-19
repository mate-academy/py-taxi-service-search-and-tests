from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestLoginRequired(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test User",
            password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_login_required(self):

        urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=(self.manufacturer.id,)),
            reverse("taxi:manufacturer-delete", args=(self.manufacturer.id,)),
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", args=(self.car.id,)),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", args=(self.car.id,)),
            reverse("taxi:car-delete", args=(self.car.id,)),
            reverse("taxi:toggle-car-assign", args=(self.car.id,)),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", args=(self.driver.id,)),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", args=(self.driver.id,)),
            reverse("taxi:driver-delete", args=(self.driver.id,)),

        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class TestIndexView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="password",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)

    def test_index_correct_template_used(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_context(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_cars"], Car.objects.count())
        self.assertEqual(
            response.context["num_drivers"],
            get_user_model().objects.count()
        )
        self.assertEqual(
            response.context["num_manufacturers"],
            Manufacturer.objects.count()
        )
        self.assertEqual(response.context["num_visits"], 1)
