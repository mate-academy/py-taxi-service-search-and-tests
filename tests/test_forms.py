from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver, Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_creation_form_with_new_fields_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ASD12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def tests_license_number_validation_with_invalid_data(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AsD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class SearchTests(TestCase):
    NUM_OBJECTS = 3

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="someuser",
            license_number="ASD12345"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):

        for manufacturer_num in range(self.NUM_OBJECTS):
            Manufacturer.objects.create(
                name=f"Lincoln{manufacturer_num}",
                country="United States"
            )
        Manufacturer.objects.create(
            name="Some_name1",
            country="Some_country1"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Lincoln"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Lincoln"))
        )

    def test_search_cars_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer1",
            country="Ukraine"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="manufacturer2",
            country="Poland"
        )
        for car_num in range(self.NUM_OBJECTS):
            Car.objects.create(
                model=f"mycar{car_num}",
                manufacturer=manufacturer
            )
        Car.objects.create(
            model="somemodel",
            manufacturer=manufacturer2
        )

        response = self.client.get(
            reverse("taxi:car-list") + "?model=mycar"
        )

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="mycar"))
        )

    def test_search_drivers_by_username(self):
        for user_num in range(self.NUM_OBJECTS):
            get_user_model().objects.create_user(
                username=f"myname{user_num}",
                license_number=f"ASD12345{user_num}"
            )

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=myname"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="myname"))
        )
