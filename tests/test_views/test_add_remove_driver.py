from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car
from django.test import TestCase
from taxi.views import add_remove_driver


class AddRemoveDriverTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer"
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.new_driver = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="WQA54321"
        )
        self.car = Car.objects.create(
            model="test car",
            manufacturer=manufacturer
        )
        self.client.force_login(self.driver)

    def test_car_detail_remove_driver_if_he_is_login_user(self):
        self.car.drivers.set([self.driver, self.new_driver])
        response = self.client.get(reverse(
            "taxi:car-detail", args=[self.car.id]
        ))
        request = response.wsgi_request
        add_remove_driver(request=request, pk=self.car.id)
        self.assertFalse(
            response.context_data["car"].drivers.filter(username="testuser")
        )

    def test_car_detail_add_driver_if_login_user_is_not_car_driver(self):
        self.car.drivers.set([self.new_driver])
        response = self.client.get(reverse(
            "taxi:car-detail", args=[self.car.id]
        ))
        request = response.wsgi_request
        add_remove_driver(request=request, pk=self.car.id)
        self.assertTrue(
            response.context_data["car"].drivers.filter(username="testuser")
        )
