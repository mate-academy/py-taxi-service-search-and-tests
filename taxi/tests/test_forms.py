from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm
from taxi.models import Driver, Car, Manufacturer


class SearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver1 = get_user_model().objects.create_user(
            username="BigBob",
            password="testpassword123",
            license_number="AXC12335",
        )
        cls.driver2 = get_user_model().objects.create_user(
            username="SmallSam",
            password="testpassword456",
            license_number="AXC12445",
        )
        cls.driver3 = get_user_model().objects.create_user(
            username="QuickQuincy",
            password="testpassword789",
            license_number="AXC12345",
        )
        cls.car1 = Car.objects.create(
            model="BMW-5",
            manufacturer=Manufacturer.objects.create(name="BMW"),
        )

        cls.car2 = Car.objects.create(
            model="Toyota Crown",
            manufacturer=Manufacturer.objects.create(name="Toyota"),
        )

        cls.car1.drivers.set([cls.driver1, cls.driver2])
        cls.car2.drivers.set([cls.driver3])

    def test_valid_driver_search_query(self):
        form = DriverSearchForm({"username": "BigBob"})
        self.assertTrue(form.is_valid())
        queryset = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"])
        self.assertIn(self.driver1, queryset)
        self.assertNotIn(self.driver2, queryset)
        self.assertNotIn(self.driver3, queryset)

    def test_invalid_driver_search_query(self):
        form = DriverSearchForm({"username": "NonExistent"})
        self.assertTrue(form.is_valid())
        queryset = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"])
        self.assertEqual(
            queryset.count(), 0,
            "The result must be empty for a non-existent name."
        )

    def test_empty_search_driver_query(self):
        form = DriverSearchForm({"username": ""})
        self.assertTrue(form.is_valid())
        queryset = Driver.objects.all()
        self.assertEqual(
            queryset.count(), 3,
            "If the field is empty, all objects should be returned."
        )

    def test_search_driver_view(self):
        self.client.login(
            username="BigBob", password="testpassword123"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "BigBob"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BigBob")
        self.assertNotContains(response, "SmallSam")
        self.assertNotContains(response, "QuickQuincy")

    def test_valid_car_search_query(self):
        form = CarSearchForm({"model": "BMW-5"})
        self.assertTrue(form.is_valid())
        queryset = Car.objects.filter(
            model__icontains=form.cleaned_data["model"])
        self.assertIn(self.car1, queryset)
        self.assertNotIn(self.car2, queryset)

    def test_invalid_car_search_query(self):
        form = CarSearchForm({"model": "NonExistent"})
        self.assertTrue(form.is_valid())
        queryset = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(queryset.count(), 0, )

    def test_search_car_view(self):
        self.client.login(
            username="BigBob", password="testpassword123"
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "BMW-5"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW-5")
        self.assertNotContains(response, "Toyota Crown")
        self.assertNotContains(response, "Toyota")

    def test_empty_manufacturers_search_query(self):
        form = ManufacturerSearchForm({"name": ""})
        self.assertTrue(form.is_valid())
        queryset = Manufacturer.objects.all()
        self.assertEqual(
            queryset.count(), 2,
            "If the field is empty, all objects should be returned."
        )

    def test_valid_manufacturer_search_query(self):
        form = ManufacturerSearchForm({"name": "BMW"})
        self.assertTrue(form.is_valid())
        queryset = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"])
        self.assertIn(self.car1.manufacturer, queryset)
        self.assertNotIn(self.car2.manufacturer, queryset)

    def test_search_manufacturer_view(self):
        self.client.login(
            username="BigBob", password="testpassword123"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")
