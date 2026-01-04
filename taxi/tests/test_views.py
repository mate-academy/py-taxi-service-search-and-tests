from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class IndexViewPublicTest(TestCase):
    def test_index_view_is_private(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)


class IndexViewPrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = Driver.objects.create(
            username="TestDriver",
            password="password",
            license_number="TEST001",
        )
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        car_1 = Car.objects.create(
            model="TestModel1",
            manufacturer=manufacturer,
        )
        car_2 = Car.objects.create(
            model="TestModel2",
            manufacturer=manufacturer,
        )
        car_1.drivers.add(driver)
        car_2.drivers.add(driver)

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="password",
        )
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("taxi:index"))

    def test_index_view_is_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_view_num_drivers_is_correct(self):
        self.assertEqual(self.response.context["num_drivers"], 2)

    def test_index_view_num_cars_is_correct(self):
        self.assertEqual(self.response.context["num_cars"], 2)

    def test_index_view_num_manufacturers_is_correct(self):
        self.assertEqual(self.response.context["num_manufacturers"], 1)

    def test_index_view_num_visits_is_correct(self):
        self.assertEqual(self.response.context["num_visits"], 1)

    def test_index_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.response,
            "taxi/index.html"
        )


class ToggleAssignToCarPublicTest(TestCase):
    def test_toggle_assign_view_is_private(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        pk = Car.objects.create(model="TestCar", manufacturer=manufacturer).pk
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": pk})
        self.response = self.client.get(url)
        self.assertNotEqual(self.response.status_code, 200)


class ToggleAssignToCarPrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        Car.objects.create(model="TestCar", manufacturer=manufacturer)

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="password",
        )
        self.client.force_login(self.user)
        self.car = Car.objects.first()
        self.url = reverse(
            "taxi:toggle-car-assign", kwargs={"pk": self.car.pk}
        )

    def test_toggle_assign_view_assigns_driver_correctly(self):
        self.client.get(self.url)
        self.assertIn(self.user, self.car.drivers.all())

    def test_toggle_assign_view_unassigns_driver_correctly(self):
        self.car.drivers.add(self.user)
        self.client.get(self.url)
        self.assertNotIn(self.user, self.car.drivers.all())

    def test_toggle_assign_view_redirect_is_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "taxi:car-detail", kwargs={"pk": self.car.pk}
        ))
