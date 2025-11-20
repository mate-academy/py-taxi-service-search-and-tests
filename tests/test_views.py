from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country 1",
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )
        Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer_1,
        )
        response = self.client.get("/")

        self.assertContains(response, "<strong>Manufacturers:</strong> 2")
        self.assertContains(response, "<strong>Cars:</strong> 1")
        self.assertContains(response, "<strong>Drivers:</strong> 1")

        response = self.client.get("/")
        self.assertEqual(response.context["num_visits"], 2)
        self.assertEqual(self.client.session["num_visits"], 2)
        self.assertContains(response, "You have visited this page 2 times.")

        response = self.client.get("/")
        self.assertEqual(response.context["num_visits"], 3)
        self.assertEqual(self.client.session["num_visits"], 3)
        self.assertContains(response, "You have visited this page 3 times.")

    def test_manufacturer_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country 1",
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, data={"name": "2"})
        self.assertContains(response, manufacturer_2.name)
        self.assertNotContains(response, manufacturer_1.name)
        self.assertIn("form", response.context)

    def test_car_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country 1",
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )
        car_1 = Car.objects.create(
            model="Test Model 1",
            manufacturer=manufacturer_1,
        )
        car_2 = Car.objects.create(
            model="Test Model 2",
            manufacturer=manufacturer_2,
        )
        url = reverse("taxi:car-list")
        response = self.client.get(url, data={"model": "2"})
        self.assertContains(response, car_2.model)
        self.assertNotContains(response, car_1.model)
        self.assertIn("form", response.context)

    def test_driver_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country 1",
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )
        car_1 = Car.objects.create(
            model="Test Model 1",
            manufacturer=manufacturer_1,
        )
        car_2 = Car.objects.create(
            model="Test Model 2",
            manufacturer=manufacturer_2,
        )
        url = reverse("taxi:car-list")
        response = self.client.get(url, data={"model": "2"})
        self.assertContains(response, car_2.model)
        self.assertNotContains(response, car_1.model)
        self.assertIn("form", response.context)

    def test_manufacturer_delete_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": manufacturer.id}
        )
        self.client.post(url)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )

    def test_car_create_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        url = reverse("taxi:car-create")
        self.client.post(url, data={
            "model": "Test Model",
            "manufacturer": manufacturer.id,
            "drivers": [self.user.id]
        })
        self.assertTrue(Car.objects.filter(model="Test Model").exists())

    def test_car_update_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Model ",
            manufacturer=manufacturer,
        )
        url = reverse("taxi:car-update", kwargs={"pk": car.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_driver_license_update_view(self):
        url = reverse("taxi:driver-update", kwargs={"pk": self.user.id})
        self.client.post(url, data={"license_number": "ABC12300"})
        self.assertEqual(
            get_user_model().objects.get(id=self.user.id).license_number,
            "ABC12300"
        )

    def test_toggle_assign_to_car_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": car.id})
        self.client.post(url)
        self.user.refresh_from_db()
        self.assertIn(car, self.user.cars.all())

        self.client.post(url)
        self.user.refresh_from_db()
        self.assertNotIn(car, self.user.cars.all())
