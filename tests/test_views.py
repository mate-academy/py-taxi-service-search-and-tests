from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

URL_LIST = [
    {'manufacturer_list_view_url': reverse('taxi:manufacturer-list')},
    {'manufacturer_create_view_url': reverse('taxi:manufacturer-create')},
    {'manufacturer_update_view_url': reverse('taxi:manufacturer-update', args=[1])},
    {'manufacturer_delete_view_url': reverse('taxi:manufacturer-delete', args=[1])},
    {'car_list_view_url': reverse('taxi:car-list')},
    {'car_detail_view_url': reverse('taxi:car-detail', args=[1])},
    {'car_create_view_url': reverse('taxi:car-create')},
    {'car_update_view_url': reverse('taxi:car-update', args=[1])},
    {'car_delete_view_url': reverse('taxi:car-delete', args=[1])},
    {'driver_list_view_url': reverse('taxi:driver-list')},
    {'driver_detail_view_url': reverse('taxi:driver-detail', args=[1])},
    {'driver_create_view_url': reverse('taxi:driver-create')},
    {'driver_update_license_view_url': reverse('taxi:driver-update', args=[1])},
    {'driver_delete_view_url': reverse('taxi:driver-delete', args=[1])},
]


class PublicViewsTest(TestCase):
    def test_login_required(self):
        for view in URL_LIST:
            for name, path in view.items():
                response = self.client.get(view[name])
                self.assertNotEqual(
                    response.status_code,
                    200,
                    f"Access to this {name} view is denied for logged out users"
                )


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="john_smith",
            password="admin.admin",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])
        self.client.force_login(self.driver)

    def test_listed_data_for_logged_users(self):
        for view in URL_LIST:
            for name, path in view.items():
                response = self.client.get(view[name])
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Access to this {name} view is should not denied for logged in users"
                )


class PrivateDriverCreateTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="john_smith",
            password="admin.admin",
        )

        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "adam_eva",
            "first_name": "adam",
            "last_name": "eva",
            "password1": "adam_eva.adam_eva",
            "password2": "adam_eva.adam_eva",
            "license_number": "AVD12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(new_driver.license_number, form_data["license_number"])
