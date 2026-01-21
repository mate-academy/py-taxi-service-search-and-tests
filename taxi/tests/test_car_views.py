from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:car-list")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_context_contains_search_form(self):
        response = self.client.get(self.url + "?model=test")
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial.get("model"), "test")

    def test_search_partial_match(self):
        Car.objects.create(model="test1", manufacturer=self.manufacturer)
        Car.objects.create(model="test2", manufacturer=self.manufacturer)

        response = self.client.get(self.url + "?model=test1")
        car_models = [car.model for car in response.context["car_list"]]
        self.assertIn("test1", car_models)
        self.assertNotIn("test2", car_models)

    def test_search_empty(self):
        Car.objects.create(model="test1", manufacturer=self.manufacturer)
        Car.objects.create(model="test2", manufacturer=self.manufacturer)

        response = self.client.get(self.url)
        car_models = [car.model for car in response.context["car_list"]]
        self.assertIn("test1", car_models)
        self.assertIn("test2", car_models)

    def test_pagination(self):
        Car.objects.bulk_create([
            Car(model=f"test{i}", manufacturer=self.manufacturer)
            for i in range(10)
        ])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_pagination_with_search(self):
        Car.objects.create(model="audi", manufacturer=self.manufacturer)
        Car.objects.bulk_create([
            Car(model=f"test{i}", manufacturer=self.manufacturer)
            for i in range(9)
        ])
        response = self.client.get(self.url + "?model=test&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 4)


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )

        self.client.force_login(self.user)
        self.url = reverse("taxi:car-create")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertEqual(response.status_code, 200)

    def test_create_car(self):
        data = {
            "model": "test",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Car.objects.count(), 1)
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_create_car_invalid(self):
        data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Car.objects.count(), 0)
        self.assertFormError(
            response.context["form"], "model", "This field is required."
        )


class CarUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )
        self.url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertEqual(response.status_code, 200)

    def test_update_car(self):
        data = {
            "model": "new_test",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        old_car_model = self.car.model
        response = self.client.post(self.url, data)
        self.car.refresh_from_db()
        self.assertNotEqual(self.car.model, old_car_model)
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_update_car_invalid(self):
        data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        old_car_model = self.car.model
        response = self.client.post(self.url, data)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, old_car_model)
        self.assertFormError(
            response.context["form"], "model", "This field is required."
        )


class CarDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer
        )
        self.url = reverse("taxi:car-delete", kwargs={"pk": self.car.id})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")
        self.assertEqual(response.status_code, 200)

    def test_delete_car(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.count(), 0)
