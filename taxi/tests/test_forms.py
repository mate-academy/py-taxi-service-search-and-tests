from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def setUp(self):
        for i in range(1, 4):
            manufacturer = Manufacturer.objects.create(
                name=f"test{i}name",
                country=f"test{i}country",
            )
            get_user_model().objects.create_user(
                username=f"test{i}",
                password=f"p@ssword123{i}",
                license_number=f"QAZ1234{i}",
            )
            Car.objects.create(
                model=f"testmodel{i}",
                manufacturer=manufacturer
            )
        self.user = get_user_model().objects.get(id=1)
        self.client.force_login(self.user)

    def test_driver_creation_with_valid_license_number_first_last_name(self):
        form_data = {
            "username": "new_user",
            "first_name": "firstuser",
            "last_name": "lastuser",
            "password1": "user123test",
            "password2": "user123test",
            "license_number": "QAZ12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_car_creation(self):
        queryset = get_user_model().objects.filter(id=1)
        manufacturer = Manufacturer.objects.get(id=1)
        form_data = {
            "model": "testmodel",
            "drivers": queryset,
            "manufacturer": manufacturer
        }
        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            form_data["manufacturer"]
        )
        self.assertEqual(
            list(form.cleaned_data["drivers"]),
            list(form_data["drivers"])
        )

    def test_license_update_form(self):
        old_license = "QAZ12345"
        new_license = "AAA00000"
        data = {"license_number": new_license}
        self.user.license_number = old_license
        self.user.save()
        form = DriverLicenseUpdateForm(instance=self.user, data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.license_number, new_license)

    def test_driver_search_form(self):
        expected_url_result = "username=2"
        expected_query_result = get_user_model().objects.filter(
            username__icontains="2"
        )
        data = {"username": "2"}
        response = self.client.get(reverse("taxi:driver-list"), data)
        url_result = response.request["QUERY_STRING"]
        query_result = response.context["object_list"]

        self.assertEqual(expected_url_result, url_result)
        self.assertEqual(list(expected_query_result), list(query_result))

    def test_car_search_form(self):
        expected_url_result = "model=1"
        expected_query_result = Car.objects.filter(model__icontains="1")
        data = {"model": "1"}
        response = self.client.get(reverse("taxi:car-list"), data)
        url_result = response.request["QUERY_STRING"]
        query_result = response.context["object_list"]

        self.assertEqual(expected_url_result, url_result)
        self.assertEqual(list(expected_query_result), list(query_result))

    def test_manufacturer_search_form(self):
        expected_url_result = "name=3"
        expected_query_result = Manufacturer.objects.filter(
            name__icontains="3"
        )
        data = {"name": "3"}
        response = self.client.get(reverse("taxi:manufacturer-list"), data)
        url_result = response.request["QUERY_STRING"]
        query_result = response.context["object_list"]

        self.assertEqual(expected_url_result, url_result)
        self.assertEqual(list(expected_query_result), list(query_result))
