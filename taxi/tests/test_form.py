from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormTest(TestCase):
    def test_driver_creation_form_with_license_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "Mari12345",
            "password2": "Mari12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ASD45678"
        }
        form = DriverCreationForm(data=form_data)
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        initial_license_number = "ASD45678"
        form_data = {
            "username": "new_user",
            "password1": "Mari12345",
            "password2": "Mari12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": initial_license_number
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        update_license_number = "ZXC54321"
        update_form_data = {
            "license_number": update_license_number
        }
        update_form = DriverLicenseUpdateForm(
            data=update_form_data,
            instance=form.instance
        )
        self.assertTrue(update_form.is_valid())
        update_form.save()
        self.assertEqual(
            update_form.clean_license_number(),
            update_license_number
        )


class SearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_user",
            password="Mari12345",
        )
        self.client.force_login(self.user)

    def test_search_manufacturer(self):
        Manufacturer.objects.create(name="Mercedes")
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Honda")
        search_url = reverse("taxi:manufacturer-list")
        search_query = "Mer"
        response = self.client.get(search_url, {"name": search_query})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Mercedes")
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Honda")

    def test_search_car(self):
        test1 = Manufacturer.objects.create(name="Mercedes")
        test2 = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="X5", manufacturer=test2)
        Car.objects.create(model="c4", manufacturer=test1)

        search_url = reverse("taxi:car-list")
        response = self.client.get(search_url, {"model": "X5"})
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, "Mercedes")
        self.assertContains(response, "BMW")

    def test_search_driver(self):
        get_user_model().objects.create(
            username="ivan",
            license_number="ASD45678"
        )
        get_user_model().objects.create(
            username="sergiy",
            license_number="QWE12345"
        )

        search_url = reverse("taxi:driver-list")
        response = self.client.get(search_url, {"username": "sergiy"})

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "sergiy")
