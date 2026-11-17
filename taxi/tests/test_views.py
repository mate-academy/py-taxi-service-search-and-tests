from django.template import engines
from django.test import RequestFactory, TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class AuthenticatedViewTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="Strong-password-123",
            license_number="ABC12345",
        )

    def test_list_views_require_login(self):
        for url_name in (
            "taxi:manufacturer-list",
            "taxi:car-list",
            "taxi:driver-list",
        ):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_list_views_are_available_after_login(self):
        self.client.force_login(self.driver)

        for url_name in (
            "taxi:manufacturer-list",
            "taxi:car-list",
            "taxi:driver-list",
        ):
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    self.client.get(reverse(url_name)).status_code,
                    200,
                )

    def test_manufacturer_list_is_paginated(self):
        self.client.force_login(self.driver)
        for number in range(6):
            Manufacturer.objects.create(
                name=f"Manufacturer {number}",
                country="Country",
            )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"page": 2}
        )

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_toggle_assign_to_car_adds_and_removes_car(self):
        self.client.force_login(self.driver)
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        car = Car.objects.create(model="Civic", manufacturer=manufacturer)
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})

        response = self.client.post(url)
        self.driver.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": car.pk}),
        )
        self.assertTrue(self.driver.cars.filter(pk=car.pk).exists())

        self.client.post(url)
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.cars.filter(pk=car.pk).exists())

    def test_query_transform_preserves_query_and_replaces_page(self):
        request = RequestFactory().get(
            "/cars/",
            {"name": "civic", "page": "1"},
        )
        template = engines["django"].from_string(
            "{% load query_transform %}"
            "{% query_transform request page=2 %}"
        )

        result = template.render({"request": request})

        self.assertIn("name=civic", result)
        self.assertIn("page=2", result)
