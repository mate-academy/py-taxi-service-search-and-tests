from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    DriverUpdateForm,
    DriverCreationForm,
    CarForm,
)
from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class CarFormTest(TestCase):

    def test_car_form_parent_class(self):
        form = CarForm
        self.assertTrue(
            issubclass(form, forms.ModelForm),
            msg="CarForm must be subclass of ModelForm",
        )

    def test_drivers_field_widget(self):
        form = CarForm()
        drivers_field = form.fields["drivers"].widget
        self.assertEqual(
            type(drivers_field),
            type(forms.CheckboxSelectMultiple()),
            msg="The widget type must be 'CheckboxSelectMultiple'"
        )

    def test_drivers_field_queryset(self):
        form = CarForm()
        drivers_field_queryset = form.fields["drivers"].queryset
        self.assertEqual(
            list(drivers_field_queryset),
            list(get_user_model().objects.all()),
        )

    def test_car_form_fields(self):
        form = CarForm()
        form_fields = form.fields
        actual_fields = [field for field in form_fields]
        required_fields = ["model", "manufacturer", "drivers"]
        self.assertEqual(
            actual_fields,
            required_fields,
        )


class DriverCreationFormTest(TestCase):

    def test_parent_class(self):
        form = DriverCreationForm
        self.assertTrue(issubclass(form, UserCreationForm))

    def test_driver_creation_form_fields(self):
        form = DriverCreationForm()
        fields = form.fields
        actual_fields_keys = [key for key in fields.keys()]
        required_fields_keys = [
            key for key in (
                UserCreationForm.Meta.fields + (
                    "license_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2"
                )
            )
        ]
        self.assertEqual(
            actual_fields_keys,
            required_fields_keys,
        )


class DriverUpdateFormTest(TestCase):
    def setUp(self):
        self.form = DriverUpdateForm
        self.data = {
            "username": "test_username",
            "license_number": "ABC12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

    def test_parent_class(self):
        self.assertTrue(
            issubclass(self.form, forms.ModelForm),
            msg="Driver license update form"
                " must be subclass of forms.ModelForm",
        )

    def test_license_number_should_consist_of_8_characters(self):
        self.data["license_number"] = "ABC123456"
        form = DriverUpdateForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )

    def test_license_number_first_three_letters_upper_case(self):
        self.data["license_number"] = "abc12345"
        form = DriverUpdateForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"][0],
            "First 3 characters should be uppercase letters"
        )

    def test_license_number_last_5_characters_is_digits(self):
        self.data["license_number"] = "ABCdef45"
        form = DriverUpdateForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"][0],
            "Last 5 characters should be digits"
        )


class DriverSearchFormTest(TestCase):
    def setUp(self):
        for i in range(3):
            license_number = f"ABC1234{i}"
            get_user_model().objects.create(
                username=f"test{i}",
                password="password",
                license_number=license_number,
            )

    def test_parent_class(self):
        form = DriverSearchForm
        self.assertTrue(
            issubclass(form, forms.Form),
            msg="Driver search form must be subclass of forms.Form"
        )

    def test_username_field_label(self):
        form = DriverSearchForm()
        label = form.fields["username"].label
        self.assertTrue(
            label == ""
            or label is None
            or label == "username"
        )

    def test_username_field_widget(self):
        form = DriverSearchForm()
        widget = form.fields["username"].widget
        placeholder = widget.attrs["placeholder"]
        self.assertEqual(
            type(widget),
            type(forms.TextInput())
        )
        self.assertEqual(
            placeholder,
            "search by username"
        )

    def test_username_field_required(self):
        form = DriverSearchForm()
        self.assertFalse(form.fields["username"].required)

    def test_username_field_max_length(self):
        form = DriverSearchForm()
        max_length = form.fields["username"].max_length
        self.assertEqual(max_length, 200)

    def test_search_driver(self):
        form = DriverSearchForm({"username": "test1"})
        self.assertTrue(form.is_valid())
        queryset = Driver.objects.filter(
            username=form.cleaned_data["username"]
        )
        self.assertEqual(
            list(queryset),
            list(Driver.objects.filter(username="test1"))
        )


class CarSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="test")
        models = ("Range Rover", "Maybach", "Skyline",)
        for model in models:
            Car.objects.create(model=model, manufacturer=manufacturer)

    def test_parent_class(self):
        form = CarSearchForm
        self.assertTrue(
            issubclass(form, forms.Form),
            msg="Car search form must be subclass of forms.Form"
        )

    def test_model_field_label(self):
        form = CarSearchForm()
        label = form.fields["model"].label
        self.assertTrue(
            label is None
            or label == ""
            or label == "model"
        )

    def test_model_field_widget(self):
        form = CarSearchForm()
        widget = form.fields["model"].widget
        placeholder = widget.attrs["placeholder"]
        self.assertEqual(type(widget), type(forms.TextInput()))
        self.assertEqual(placeholder, "Search by model")

    def test_model_field_required(self):
        form = CarSearchForm()
        is_required = form.fields["model"].required
        self.assertFalse(is_required)

    def test_model_field_max_length(self):
        form = CarSearchForm()
        max_length = form.fields["model"].max_length
        self.assertEqual(max_length, 200)

    # ???
    def test_search_car(self):
        form = CarSearchForm({"model": "Range"})
        self.assertTrue(form.is_valid())
        queryset = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(
            list(queryset),
            list(Car.objects.filter(model__icontains="Range"))
        )


class ManufactureSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufactures = ("Dodge", "BMW", "Toyota",)
        for manufacturer in manufactures:
            Manufacturer.objects.create(name=manufacturer)

    def test_parent_class(self):
        form = ManufacturerSearchForm
        self.assertTrue(
            issubclass(form, forms.Form),
            msg="Manufacturer search form must be subclass of forms.Form"
        )

    def test_name_field_label(self):
        form = ManufacturerSearchForm()
        label = form.fields["name"].label
        self.assertTrue(
            label is None
            or label == ""
            or label == "name"
        )

    def test_name_field_widget(self):
        form = ManufacturerSearchForm()
        widget = form.fields["name"].widget
        placeholder = widget.attrs["placeholder"]
        self.assertEqual(type(widget), type(forms.TextInput()))
        self.assertEqual(placeholder, "Search by manufacturer")

    def test_name_field_required(self):
        form = ManufacturerSearchForm()
        is_required = form.fields["name"].required
        self.assertFalse(is_required)

    def test_name_field_max_length(self):
        form = ManufacturerSearchForm()
        max_length = form.fields["name"].max_length
        self.assertEqual(max_length, 200)

    def test_search_manufacturer(self):
        form = ManufacturerSearchForm({"name": "Dodge"})
        self.assertTrue(form.is_valid())
        queryset = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(
            list(queryset),
            list(Manufacturer.objects.filter(
                name__icontains="Dodge"
            ))
        )
