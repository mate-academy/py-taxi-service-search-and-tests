from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm, ManufacturerSearchForm, DriverSearchForm
from taxi.models import Car, Manufacturer, Driver


class SearchFormTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="Chi",
            password="12345",
            license_number="ACV12345"
        )
        self.client.force_login(user)
        toyota = Manufacturer.objects.create(name="Toyota", country="Ukraine")
        chucho = Manufacturer.objects.create(name="Chucho", country="Ukraine")
        speed = Manufacturer.objects.create(name="Speed", country="Ukraine")
        Car.objects.create(model="Lancer", manufacturer=toyota)
        Car.objects.create(model="Civic", manufacturer=chucho)
        Car.objects.create(model="Accord", manufacturer=speed)

    def test_car_search_form(self):
        model = "Lancer"
        form_data = {
            "model": model
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.get(
            reverse("taxi:car-list"),
            data=form.cleaned_data
        )
        expected_cars = Car.objects.filter(model__icontains=model)

        self.assertEqual(
            list(response.context["car_list"]),
            list(expected_cars)
        )

    def test_manufacturer_search_form(self):
        name = "Speed"
        form_data = {
            "name": name
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data=form.cleaned_data
        )
        expected_cars = Manufacturer.objects.filter(name__icontains=name)

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(expected_cars)
        )

    def test_driver_search_form(self):
        username = "Chi"
        form_data = {
            "username": username
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.get(
            reverse("taxi:driver-list"),
            data=form.cleaned_data
        )
        expected_cars = Driver.objects.filter(username__icontains=username)

        self.assertEqual(
            list(response.context["driver_list"]),
            list(expected_cars)
        )
