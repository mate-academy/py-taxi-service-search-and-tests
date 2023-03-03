from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.views import toggle_assign_to_car
from taxi.models import Car, Manufacturer


class AddRemoveDriverTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="Ukraine"
        )
        self.driver = get_user_model().objects.create_user(
            username="test driver",
            password="test12345"
        )
        self.another_driver = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="RED12345"
        )
        self.car = Car.objects.create(
            model="test car",
            manufacturer=manufacturer
        )
        self.client.force_login(self.driver)

    def test_car_detail_remove_driver_if_he_is_login_user(self):
        self.car.drivers.add(self.driver, self.another_driver)
        response = self.client.get(reverse(
            "taxi:car-detail", kwargs={"pk": self.car.id}
        ))
        request = response.wsgi_request
        toggle_assign_to_car(request=request, pk=self.car.id)

        self.assertFalse(
            response.context_data["car"].drivers.filter(username="test driver")
        )

    def test_car_detail_add_driver_if_login_user_is_not_car_driver(self):
        self.car.drivers.add(self.another_driver)
        response = self.client.get(reverse(
            "taxi:car-detail", kwargs={"pk": self.car.id}
        ))
        request = response.wsgi_request
        toggle_assign_to_car(request=request, pk=self.car.id)

        self.assertTrue(
            response.context_data["car"].drivers.filter(username="test driver")
        )
