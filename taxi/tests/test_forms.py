from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverSearchForm, CarSearchForm
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test", password="test_test"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        Driver.objects.create(username="user1", license_number="ABC12345")
        Driver.objects.create(username="user2", license_number="ABC54321")

        response = self.client.get(reverse("taxi:driver-list"), {"username": "user2"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], DriverSearchForm)
        self.assertQuerysetEqual(
            response.context["object_list"],
            Driver.objects.filter(username__icontains="user2"),
        )

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="testmanufacturer")
        driver = get_user_model().objects.create(
            username="driver1",
            password="test_test",
            first_name="test_firstname",
            last_name="test_lastname",
            license_number="ABC12345",
        )
        car1 = Car.objects.create(model="car1", manufacturer=manufacturer)
        car2 = Car.objects.create(model="car2", manufacturer=manufacturer)
        car1.drivers.set([driver])
        car2.drivers.set([driver])

        response = self.client.get(reverse("taxi:car-list"), {"model": "car1"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertQuerysetEqual(
            response.context["object_list"],
            Car.objects.filter(model__icontains="car1"),
        )


#
