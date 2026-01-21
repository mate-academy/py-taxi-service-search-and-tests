from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import ManufacturerNameSearchForm, CarModelSearchForm
from taxi.models import Manufacturer, Car


class ManufacturerSearchFormTest(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="A", country="test")
        Manufacturer.objects.create(name="AA", country="test")
        Manufacturer.objects.create(name="B", country="test")
        Manufacturer.objects.create(name="Bb", country="test")

    def test_form_valid_data(self):
        form = ManufacturerNameSearchForm(data={"name": "a"})
        self.assertTrue(form.is_valid())
        name = form.cleaned_data["name"]
        manufacturers = Manufacturer.objects.filter(name__icontains=name)
        self.assertEqual(manufacturers.count(), 2)

    def test_form_without_data(self):
        form = ManufacturerNameSearchForm(data={})
        self.assertTrue(form.is_valid())
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(Manufacturer.objects.all()), list(manufacturers))
