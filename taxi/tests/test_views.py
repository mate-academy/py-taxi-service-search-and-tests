from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        cls.driver = get_user_model().objects.create_user(
            username="test", license_number="TES12345"
        )
        cls.car = Car.objects.create(
            model="TestCar", manufacturer=cls.manufacturer
        )

    def test_login_required_for_protected_pages(self):
        urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=[self.manufacturer.pk]),
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.pk]),
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", args=[self.car.pk]),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", args=[self.car.pk]),
            reverse("taxi:car-delete", args=[self.car.pk]),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", args=[self.driver.pk]),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", args=[self.driver.pk]),
            reverse("taxi:driver-delete", args=[self.driver.pk]),
            reverse("taxi:toggle-car-assign", args=[self.car.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)


class PrivatePagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="VAL98765"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        get_user_model().objects.create_user(
            username="another_user", license_number="ANO12345"
        )
        Car.objects.create(model="Model X", manufacturer=cls.manufacturer)
        Manufacturer.objects.create(name="Ford", country="USA")
        cls.car_s = Car.objects.create(
            model="Model S",
            manufacturer=cls.manufacturer
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_retrieve_list_views(self):
        urls_and_templates = {
            "driver_list": reverse("taxi:driver-list"),
            "car_list": reverse("taxi:car-list"),
            "manufacturer_list": reverse("taxi:manufacturer-list"),
        }
        for template, url in urls_and_templates.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f"taxi/{template}.html")

    def test_search_form_in_context(self):
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn("search_form", response.context)

    def test_search_functionality(self):
        search_scenarios = [
            {
                "model_name": "Driver",
                "url": reverse("taxi:driver-list"),
                "search_param": {"username": "testuser"},
                "expected_object": self.driver,
            },
            {
                "model_name": "Car",
                "url": reverse("taxi:car-list"),
                "search_param": {"model": "Model S"},
                "expected_object": self.car_s,
            },
            {
                "model_name": "Manufacturer",
                "url": reverse("taxi:manufacturer-list"),
                "search_param": {"name": "Tesla"},
                "expected_object": self.manufacturer,
            },
        ]

        for scenario in search_scenarios:
            with self.subTest(model=scenario["model_name"]):
                response = self.client.get(
                    scenario["url"],
                    scenario["search_param"]
                )
                queryset = response.context["object_list"]
                self.assertEqual(queryset.count(), 1)
                self.assertIn(scenario["expected_object"], queryset)

    def test_toggle_assign_car_view(self):
        car = Car.objects.create(
            model="TestCar",
            manufacturer=self.manufacturer
        )
        toggle_url = reverse("taxi:toggle-car-assign", args=[car.pk])

        with self.subTest(action="assign"):
            response = self.client.post(toggle_url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(car, self.driver.cars.all())

        with self.subTest(action="unassign"):
            response = self.client.post(toggle_url)
            self.driver.refresh_from_db()
            self.assertEqual(response.status_code, 302)
            self.assertNotIn(car, self.driver.cars.all())
