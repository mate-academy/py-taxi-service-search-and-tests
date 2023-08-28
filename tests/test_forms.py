from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )

        self.client.force_login(self.user)

    def test_driver_creation_is_valid(self):
        form_data = {
            "username": "new_driver",
            "password1": "driver12345",
            "password2": "driver12345",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.username,
            form_data["username"]
        )
        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_search_form_is_work_in_car_list(self):
        text_to_filter = "M3"
        data = {
            "model": text_to_filter
        }

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="M3", manufacturer=manufacturer)
        Car.objects.create(model="M4", manufacturer=manufacturer)
        Car.objects.create(model="M5", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-list"), data=data)

        cars_after_filter_on_page = response.context_data["car_list"]
        cars_to_filter = Car.objects.filter(model=data["model"])

        self.assertEqual(
            list(cars_after_filter_on_page),
            list(cars_to_filter)
        )

    def test_search_form_is_work_in_manufacturer_list(self):
        text_to_filter = "BMW"
        data = {
            "name": text_to_filter
        }

        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(reverse(
            "taxi:manufacturer-list"
        ), data=data)

        manufacturers_list_on_page = response.context_data["manufacturer_list"]
        manufacturers_to_filter = Manufacturer.objects.filter(
            name=data["name"]
        )

        self.assertEqual(
            list(manufacturers_list_on_page),
            list(manufacturers_to_filter)
        )

    def test_search_form_is_work_in_driver_list(self):
        text_to_filter = "new_driver"
        data = {
            "username": text_to_filter
        }

        get_user_model().objects.create_user(
            username="new_driver",
            password="test1234",
            license_number="ACB12345"

        )
        get_user_model().objects.create_user(
            username="new_driver2",
            password="test1234",
            license_number="CAB12345"

        )

        response = self.client.get(reverse("taxi:driver-list"), data=data)

        drivers_after_filter_on_page = response.context_data["driver_list"]
        drivers_to_filter = get_user_model().objects.filter(
            username__contains=data["username"]
        )

        self.assertEqual(
            list(drivers_after_filter_on_page),
            list(drivers_to_filter)
        )
