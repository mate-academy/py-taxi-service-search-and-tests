from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car


class TestCreateAndDeleteModels(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tset",
            password="test12345",
        )

        self.client.force_login(user)

    def test_form_should_create_driver(self):
        data = {
            "username": "test",
            "license_number": "ABC12345",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "",
            "last_name": "",
        }

        form = DriverCreationForm(data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_should_create_manufacturer(self):
        before_post = len(Manufacturer.objects.all())

        self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "test-name", "country": "test-country"},
        )

        after_post = len(Manufacturer.objects.all())

        self.assertNotEqual(before_post, after_post)

    def test_should_create_car(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test_country")
        before_post = Car.objects.all()

        self.client.post(
            reverse("taxi:manufacturer-create"),
            {"model": "test-model", "manufacturer": manufacturer},
        )

        after_post = Car.objects.all()

        self.assertNotEqual(before_post, after_post)

