from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tset",
            password="test12345",
        )

        self.client.force_login(self.user)

    def test_search_form_for_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test3",
            manufacturer=manufacturer
        )
        car = Car.objects.filter(model="test3")
        response = self.client.get(reverse("taxi:car-list") + "?form=test3")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(car))

    def test_search_form_for_driver(self):
        Driver.objects.create(
            username="test", password="test12345", license_number="ABC12345"
        )
        Driver.objects.create(
            username="test1", password="test12345", license_number="ABD12345"
        )
        # drivers = Driver.objects.all()
        driver = Driver.objects.filter(username="test1")

        response = self.client.get(
            reverse("taxi:driver-list") + "?form=test1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(list(response.context["driver_list"]), list(driver))

    def test_search_form_for_manufacturer(self):
        Manufacturer.objects.create(
            name="test1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test2",
            country="test_country2"
        )
        manufacturer = Manufacturer.objects.filter(name="test2")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?form=test2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )


class TestToggle(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="test_driver", password="password",
            first_name="John", last_name="Doe",
            license_number="ABC12345"
        )

    def test_toggle_assign_to_car_assign(self):
        # Try to assign a driver to a car
        self.client.force_login(self.driver)
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car.drivers.filter(id=self.driver.id).exists())

    def test_toggle_assign_to_car_delete(self):
        # Assign a driver to the car and then try to remove them
        self.car.drivers.add(self.driver)
        self.client.force_login(self.driver)
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.car.drivers.filter(id=self.driver.id).exists())
