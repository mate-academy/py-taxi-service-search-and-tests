from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car, Driver
from taxi.views import ManufacturerListView


class TestSearchForm(TestCase):

    def setUp(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer 1", country="Test Country"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer 2", country="Test Country 2"
        )

        Car.objects.create(
            model="Test Car 1", manufacturer=manufacturer1
        )
        Car.objects.create(
            model="Test Car 2", manufacturer=manufacturer2
        )

        Driver.objects.create(
            username="testdriver1",
            license_number="TRE12345",
        )
        Driver.objects.create(
            username="testdriver2",
            license_number="TRG12345",
        )

    def data_for_test(
            self, form_data: dict, expected_data: int | None = None
    ) -> None:

        form_manufacturer = ManufacturerSearchForm(data=form_data)
        form_driver = DriverSearchForm(data=form_data)
        form_car = CarSearchForm(data=form_data)

        self.assertTrue(form_manufacturer.is_valid())
        self.assertTrue(form_driver.is_valid())
        self.assertTrue(form_car.is_valid())


    def test_form_with_valid_data(self):
        form_data = {"title": "Test Manufacturer"}
        self.data_for_test(form_data)

    def test_form_with_empty_data(self):
        form_data = {}
        self.data_for_test(form_data)

    def test_form_with_long_title(self):
        form_data = {"title": "A" * 256}
        form = ManufacturerSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_manufacturer_search_form(self):
        search_scenarios = [
            {"title": "Test Manufacturer 1", "expected_result_count": 1},
            {"title": "Test", "expected_result_count": 2},
            {"title": "Test Manufacturer 3", "expected_result_count": 0}
        ]

        for scenario in search_scenarios:
            form_data = {"title": scenario["title"]}
            form = ManufacturerSearchForm(data=form_data)

            self.assertTrue(form.is_valid())

            queryset = Manufacturer.objects.all()

            search_result = queryset.filter(
                name__icontains=form.cleaned_data["title"]
            )

            self.assertEqual(
                len(search_result), scenario["expected_result_count"]
            )

    def test_car_search_form(self):
        search_scenarios = [
            {"title": "Test Car 1", "expected_result_count": 1},
            {"title": "Test", "expected_result_count": 2},
            {"title": "Test Car 3", "expected_result_count": 0}
        ]

        for scenario in search_scenarios:
            form_data = {"title": scenario["title"]}
            form = CarSearchForm(data=form_data)

            self.assertTrue(form.is_valid())

            queryset = Car.objects.all()

            search_result = queryset.filter(
                model__icontains=form.cleaned_data["title"]
            )

            self.assertEqual(
                len(search_result), scenario["expected_result_count"]
            )

    def test_driver_search_form(self):
        search_scenarios = [
            {"title": "testdriver1", "expected_result_count": 1},
            {"title": "test", "expected_result_count": 2},
            {"title": "testdriver3", "expected_result_count": 0}
        ]

        for scenario in search_scenarios:
            form_data = {"title": scenario["title"]}
            form = DriverSearchForm(data=form_data)

            self.assertTrue(form.is_valid())

            queryset = Driver.objects.all()

            search_result = queryset.filter(
                username__icontains=form.cleaned_data["title"]
            )

            self.assertEqual(
                len(search_result), scenario["expected_result_count"]
            )
