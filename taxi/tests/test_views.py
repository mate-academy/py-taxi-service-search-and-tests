from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="user12test"
        )
        self.client.force_login(self.user)
        self.form_data = {
            "name": "newmanufacturer",
            "country": "italy"
        }
        self.client.post(reverse("taxi:manufacturer-create"), self.form_data)
        self.new_manufacturer = Manufacturer.objects.get(
            name=self.form_data["name"])


class PrivateIndexTest(BaseTestCase):
    def test_index_context(self):
        response1 = self.client.get(INDEX_URL)
        self.assertEqual(response1.context["num_visits"], 1)
        response2 = self.client.get(INDEX_URL)
        self.assertEqual(response2.context["num_visits"], 2)
        keys = ["num_drivers", "num_cars", "num_manufacturers"]
        for key in keys:
            self.assertIn(key, response1.context)
        self.assertTemplateUsed(response1, "taxi/index.html")


class PrivateManufacturerTests(BaseTestCase):

    def test_create_manufacturer(self):
        self.assertEqual((self.new_manufacturer.name,
                          self.new_manufacturer.country),
                         (self.form_data["name"],
                          self.form_data["country"]))

    def test_manufacturer_list_context(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "test"})
        self.assertIn("search_form", res.context)
        form = res.context["search_form"]
        self.assertEqual(form.initial["name"], "test")


class PrivateDriverTests(BaseTestCase):

    def test_create_driver(self):
        form_data = {
            "username": "newuser",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test",
            "last_name": "user",
            "license_number": "URI15264",
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        new_user = get_user_model().objects.get(
            username=form_data["username"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertEqual((
            new_user.first_name,
            new_user.last_name,
            new_user.username),
            (form_data["first_name"],
             form_data["last_name"],
             form_data["username"]))

    def test_driver_list_context(self):
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"})
        self.assertIn("search_form", res.context)
        form = res.context["search_form"]
        self.assertEqual(form.initial["username"], "test")


class PrivateCarTests(BaseTestCase):

    def test_create_car(self):
        form_data = {
            "model": "newcar",
            "manufacturer" : self.new_manufacturer.id,
            "drivers": [self.user.id]
        }

        self.client.post(reverse("taxi:car-create"), form_data)
        new_car = Car.objects.get(model=form_data["model"])
        self.assertEqual((new_car.model,
                          new_car.manufacturer),
                         (form_data["model"],
                          Manufacturer.objects.get(
                              id=form_data["manufacturer"])))

    def test_car_list_context(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "test"})
        self.assertIn("search_form", res.context)
        form = res.context["search_form"]
        self.assertEqual(form.initial["model"], "test")

    def test_driver_assign_into_car(self):
        form_data = {
            "model": "newcar",
            "manufacturer": self.new_manufacturer.id,
            "drivers": []
        }
        Car.objects.create(
            model=form_data["model"],
            manufacturer=self.new_manufacturer)
        new_car = Car.objects.get(model=form_data["model"])
        driver = get_user_model().objects.get(id=self.user.id)
        self.client.get(reverse("taxi:toggle-car-assign", args=[new_car.id]))
        self.assertIn(new_car, driver.cars.all())
        self.client.get(reverse("taxi:toggle-car-assign", args=[new_car.id]))
        self.assertNotIn(new_car, driver.cars.all())
