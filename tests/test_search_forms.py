from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import CarSearchForm, ManufacturerSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car


class BasePlaceholderTest(TestCase):
    def assert_placeholder(
            self,
            form_class,
            field_name,
            expected_placeholder
    ):
        form = form_class()
        self.assertIn(field_name, form.fields)
        self.assertEqual(
            form.fields[field_name].widget.attrs.get(
                "placeholder"
            ),
            expected_placeholder,
        )


class BaseSearchTest(TestCase):
    def assert_search_result(
            self,
            form_class,
            search_field,
            search_data,
            expected_data
    ):
        form = form_class(data=search_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data[search_field], expected_data
        )


class DriverSearchFormTest(BaseSearchTest):
    def setUp(self):
        get_user_model().objects.create_user(
            username="admin_user",
            password="87ASDHADIK7asd7IA6SD",
            first_name="Mike",
            last_name="Smith",
            license_number="AAA1111",
        )

    def test_search(self):
        self.assert_search_result(
            form_class=DriverSearchForm,
            search_field="username",
            search_data={"username": "admin_user"},
            expected_data="admin_user",
        )


class CarSearchFormTest(BaseSearchTest, BasePlaceholderTest):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ferrari", country="Italy"
        )
        self.car = Car.objects.create(
            model="F8 Spider",
            manufacturer=self.manufacturer,
        )

    def test_search(self):
        self.assert_search_result(
            form_class=CarSearchForm,
            search_field="model",
            search_data={"model": "F8 Spider"},
            expected_data="F8 Spider",
        )

    def test_placeholder(self):
        self.assert_placeholder(
            CarSearchForm,
            "model",
            "Search by model"
        )


class ManufacturerSearchFormTest(BasePlaceholderTest):
    def test_placeholder(self):
        self.assert_placeholder(
            ManufacturerSearchForm,
            "name",
            "Search by name"
        )
