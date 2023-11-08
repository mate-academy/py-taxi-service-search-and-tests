from django.test import TestCase
from parameterized import parameterized
from taxi.models import Manufacturer, Car, Driver
from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)


class SearchFeatureTest(TestCase):
    def setUp(self) -> None:
        self.items = [
            "Test something", "Test anything", "Test"
        ]

        i = 0
        for name in self.items:
            manufacturer = Manufacturer.objects.create(
                name=name, country="test_country"
            )
            Car.objects.create(
                model=name,
                manufacturer=manufacturer
            )
            Driver.objects.create_user(
                username=name,
                password="password123456",
                license_number=f"ABC1234{i}",
            )
            i += 1

    @parameterized.expand([
        (Car, CarSearchForm, "model"),
        (Manufacturer, ManufacturerSearchForm, "name"),
        (Driver, DriverSearchForm, "username")
    ])
    def test_partial_search(
            self,
            model: (Car, Manufacturer, Driver),
            form: (
                CarSearchForm,
                ManufacturerSearchForm,
                DriverSearchForm
            ),
            field_name: str
    ) -> None:
        form_data = {
            field_name: "ing",
        }

        form = form(data=form_data)
        self.assertTrue(form.is_valid())

        results = model.objects.filter(
            **{f"{field_name}__icontains": form.cleaned_data[field_name]}
        )

        expected_names = ["Test something", "Test anything"]

        self.assertCountEqual(
            [
                getattr(item, field_name)
                for item in results
            ], expected_names
        )
