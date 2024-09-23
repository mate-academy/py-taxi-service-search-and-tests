from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from taxi.forms import ManufacturerSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car


class ManufacturerSearchFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testtt1234",
            password="test123",
            license_number="CCC12345"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="test")
        Manufacturer.objects.create(name="Honda", country="test")
        Manufacturer.objects.create(name="Ford1", country="test")
        Manufacturer.objects.create(name="Ford2", country="test")
        Manufacturer.objects.create(name="Ford3", country="test")
        Manufacturer.objects.create(name="Ford4", country="test")

    def test_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "ford"})
        self.assertTrue(form.is_valid())
        name = form.cleaned_data["name"]
        manufacturers = Manufacturer.objects.filter(name__icontains=name)
        self.assertEqual(manufacturers.count(), 4)
        self.assertEqual(manufacturers.first().name, "Ford1")

    def test_form_without_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(Manufacturer.objects.all()), list(manufacturers))
        self.assertEqual(Manufacturer.objects.count(), manufacturers.count())

    def test_form_invalid_data(self):
        form = ManufacturerSearchForm(data={"name": "NonExistent"})
        self.assertTrue(form.is_valid())
        name = form.cleaned_data["name"]
        manufacturers = Manufacturer.objects.filter(name__icontains=name)
        self.assertEqual(manufacturers.count(), 0)


class CarSearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test12345tt",
            password="test123",
            license_number="BBB12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="testname")
        Car.objects.create(model="test1", manufacturer=self.manufacturer)
        Car.objects.create(model="test2", manufacturer=self.manufacturer)
        Car.objects.create(model="test3", manufacturer=self.manufacturer)
        Car.objects.create(model="test4", manufacturer=self.manufacturer)
        Car.objects.create(model="test5", manufacturer=self.manufacturer)
        Car.objects.create(model="test6", manufacturer=self.manufacturer)
        Car.objects.create(model="sss223", manufacturer=self.manufacturer)

    def test_form_valid_data(self):
        form = CarSearchForm(data={"model": "test"})
        self.assertTrue(form.is_valid())
        model = form.cleaned_data["model"]
        cars = Car.objects.filter(model__icontains=model)
        self.assertEqual(cars.count(), 6)
        self.assertEqual(cars.first().model, "test1")

    def test_form_without_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        cars = Car.objects.all()
        self.assertEqual(list(Car.objects.all()), list(cars))
        self.assertEqual(Car.objects.count(), cars.count())

    def test_form_invalid_data(self):
        form = CarSearchForm(data={"model": "NonExistent"})
        self.assertTrue(form.is_valid())
        model = form.cleaned_data["model"]
        cars = Car.objects.filter(model__icontains=model)
        self.assertEqual(cars.count(), 0)
