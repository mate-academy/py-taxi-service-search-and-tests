from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer
from taxi.forms import (CarSearchForm,
                        DriverSearchForm,
                        ManufacturerSearchForm,
                        DriverCreationForm
                        )

User = get_user_model()


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="testuser",
            password="testpassword",
            license_number="ABC12345",
        )
        self.user2 = get_user_model().objects.create(
            username="new_user",
            password="newpassword",
            license_number="CBA54321",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="F150",
            manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Highlander",
            manufacturer=self.manufacturer1
        )

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "camry"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "amr"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_manufacturer_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)

    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "testuser"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, self.user2.username)
        self.assertContains(response, self.user.license_number)
        self.assertNotContains(response, self.user2.license_number)

        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "est"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, self.user2.username)
        self.assertContains(response, self.user.license_number)
        self.assertNotContains(response, self.user2.license_number)

        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "TESTUSer"})
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, self.user2.username)


class FormsTest(TestCase):
    def test_driver_creation_form_with_username_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "new_user")
        self.assertEqual(form.cleaned_data["first_name"], "Test first")
        self.assertEqual(form.cleaned_data["last_name"], "Test last")
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")
