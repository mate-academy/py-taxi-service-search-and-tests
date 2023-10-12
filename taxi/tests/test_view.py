from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 10
        for driver_id in range(number_of_drivers):
            Driver.objects.create(
                first_name=f"test {driver_id}",
                last_name=f"surname {driver_id}",
                license_number=f"TTT1{(driver_id+1) % 10}34{driver_id % 10}",
                username=f"username {driver_id}",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_url_all_drivers_exist(self):
        response = self.client.get("/drivers/")
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEquals(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_is_2(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEquals(len(response.context["driver_list"]), 2)

    def test_page_6_with_one_driver(self):
        response = self.client.get(reverse("taxi:driver-list") + "?page=6")
        self.assertEquals(len(response.context["driver_list"]), 1)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "license_number": "AAA12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = Driver.objects.get(username=form_data["username"])

        self.assertEquals(new_driver.username, form_data["username"])
        self.assertEquals(new_driver.last_name, form_data["last_name"])
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        Car.objects.create(model="Opel", manufacturer=manufacturer)
        Car.objects.create(model="Nissan", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEquals(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEquals(list(response.context["car_list"]), list(cars))


class CarSearchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        models = [
            "nissan",
            "opel",
            "volskvagen",
            "mercedes",
            "kia",
            "shevrolet",
            "renault"
        ]
        for model in models:
            Car.objects.create(model=model, manufacturer=manufacturer)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_search_model_car_with_single_letter(self):
        char = "a"
        response = self.client.get(f"/cars/?model={char}")
        car_with_letter_a = Car.objects.filter(model__icontains=char)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_with_letter_a)[:3]
        )

    def test_search_model_car_with_uppercase_letters(self):
        char = "AN"
        response = self.client.get(f"/cars/?model={char}")
        car_with_letter_a = Car.objects.filter(model__icontains=char)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_with_letter_a)[:3]
        )

    def test_search_model_car_page_2(self):
        char = "A"
        response = self.client.get(f"/cars/?model={char}&page=2")
        car_with_letter_a = Car.objects.filter(model__icontains=char)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_with_letter_a)[3:6]
        )

    def test_search_model_car_by_exact_name(self):
        response = self.client.get("/cars/?model=opel")
        opel = Car.objects.filter(model="opel")
        self.assertEquals(list(response.context["car_list"]), list(opel))
