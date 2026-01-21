from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class TestPublicIndexPage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_context_list(self):
        response = self.client.get("/")
        context_list = [
            "num_drivers", "num_cars", "num_manufacturers", "num_visits",
        ]
        for context_name in context_list:
            self.assertIn(context_name, response.context)

    def test_visits_counter(self):
        num_visits = 4
        for i in range(num_visits):
            response = self.client.get("/")
        self.assertEqual(response.context["num_visits"], num_visits)

    def test_models_records_count(self):
        num_drivers = 4
        num_cars = 2
        num_manufacturers = 6
        for i in range(num_manufacturers):
            Manufacturer.objects.create(name="name{}".format(i))
        for i in range(num_cars):
            Car.objects.create(
                model="car{}".format(i),
                manufacturer=Manufacturer.objects.get(id=i + 1)
            )
        for i in range(num_drivers):
            get_user_model().objects.create_user(
                username="driver{}".format(i),
                password="pass_{}".format(i),
                license_number="ABC1234{}".format(i),
            )
        response = self.client.get("/")

        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"], num_manufacturers
        )


class TestRestrictedPages(TestCase):
    NUM_DRIVERS = 7
    NUM_CARS = 11
    NUM_MANUFACTURERS = 6
    KWARGS = {"pk": 1}

    def setUp(self):

        for manufacturer_index in range(self.NUM_MANUFACTURERS):
            Manufacturer.objects.create(name=f"name_{manufacturer_index}")

        for car_index in range(self.NUM_CARS):
            Car.objects.create(
                model=f"car{car_index}",
                manufacturer=Manufacturer.objects.get(
                    id=car_index % self.NUM_MANUFACTURERS + 1
                )
            )
        for driver_index in range(self.NUM_DRIVERS):
            get_user_model().objects.create_user(
                username=f"driver_{driver_index}",
                password=f"passwrd_{driver_index}",
                license_number=f"ABC8234{driver_index}"
            )

        for car in Car.objects.all():
            car.drivers.add(get_user_model().objects.get(id=1))

        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="PASSWORD",
        )
        self.client.force_login(self.user)
        self.NUM_DRIVERS += 1

    def test_unlogged_user_redirect(self):
        unlogged_client = Client()
        route_names = [
            "taxi:driver-list",
            "taxi:car-list",
            "taxi:manufacturer-list",
        ]
        for route_name in route_names:
            response = unlogged_client.get(reverse(route_name))
            expected_url = reverse("login") + f"?next={reverse(route_name)}"
            self.assertRedirects(response, expected_url)

    def test_logged_user_list_view_response_code(self):
        route_names = [
            ("taxi:driver-list", "taxi/driver_list.html"),
            ("taxi:car-list", "taxi/car_list.html"),
            ("taxi:manufacturer-list", "taxi/manufacturer_list.html"),
        ]
        for route_name, template_name in route_names:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)

    def test_logged_user_detail_view_response_code(self):
        route_names = [
            ("taxi:driver-detail", "taxi/driver_detail.html"),
            ("taxi:car-detail", "taxi/car_detail.html"),
        ]
        for route_name, template_name in route_names:
            response = self.client.get(reverse(route_name, kwargs=self.KWARGS))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)

    def test_car_detail_view_(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs=self.KWARGS)
        )
        self.assertIn("car", response.context)
        self.assertEqual(
            response.context["car"].model,
            Car.objects.get(id=self.KWARGS["pk"]).model
        )
        self.assertEqual(
            response.context["car"].manufacturer.name,
            Car.objects.get(id=self.KWARGS["pk"]).manufacturer.name
        )

    def test_driver_detail_view_(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs=self.KWARGS)
        )
        self.assertIn("driver", response.context)
        self.assertEqual(
            response.context["driver"].username,
            get_user_model().objects.get(id=self.KWARGS["pk"]).username
        )
        self.assertEqual(
            response.context["driver"].license_number,
            get_user_model().objects.get(id=self.KWARGS["pk"]).license_number
        )
        self.assertEqual(
            list(response.context["driver"].cars.all()),
            list(get_user_model().objects.get(id=self.KWARGS["pk"]).cars.all())
        )

    def pagination_car_page_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(len(response.context["car_list"]), 5)
        response = self.client.get(reverse("taxi:car-list") + "?page=2")
        self.assertEqual(len(response.context["car_list"]), self.NUM_CARS % 5)
