from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        Car.objects.create(model="Test 1", manufacturer=manufacturer)
        Car.objects.create(model="Test 2", manufacturer=manufacturer)

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_login_required_car_detail(self):
        car_detail = Car.objects.get(pk=1)
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": car_detail.pk})
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/cars/1/")

    def test_login_required_creation_car_form(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/cars/create/")


class PrivateCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        for car_id in range(8):
            Car.objects.create(
                model=f"Test {car_id}",
                manufacturer=manufacturer
            )
        get_user_model().objects.create_user(
            username="test_1",
            password="test password123",
            license_number="QWE12345"
        )
        get_user_model().objects.create_user(
            username="test_2",
            password="test password123",
            license_number="XSW12345"
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test password"
        )
        self.client.force_login(self.user)

    def test_cars_pagination_is_five(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_cars_pagination_second_page(self):
        response = self.client.get(CAR_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 3)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        car_detail = Car.objects.get(pk=1)
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": car_detail.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_toggle_assign_to_car(self):
        new_car = Car.objects.get(pk=1)
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": new_car.pk}
        ))
        self.assertNotContains(response, "Delete me from this car")
        self.assertContains(response, "Assign me from this car")

        self.user.cars.add(new_car)
        response = self.client.get(reverse(
            "taxi:car-detail", kwargs={"pk": new_car.pk}
        ))
        self.assertContains(response, "Delete me from this car")
        self.assertNotContains(response, "Assign me from this car")

    def test_car_creation(self):
        manufacturer_1 = Manufacturer.objects.get(pk=1)
        driver_1 = get_user_model().objects.get(pk=1)
        driver_2 = get_user_model().objects.get(pk=2)
        form_data = {
            "model": "test model",
            "manufacturer": manufacturer_1.id,
            "drivers": [driver_1.id, driver_2.id]
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer, manufacturer_1)
        self.assertEqual(list(new_car.drivers.all()), [driver_1, driver_2])

    def test_delete_car(self):
        car = Car.objects.get(pk=1)
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=car.id).exists())

    def test_car_search_matches_found(self):
        response = self.client.get("/cars/?model=test+2")
        searching_car = Car.objects.filter(model="Test 2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(searching_car)
        )

    def test_car_search_no_matches_found(self):
        response = self.client.get("/cars/?model=Fake+name")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars in taxi")
