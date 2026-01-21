from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth import get_user_model


class ManufacturerTestView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        Manufacturer.objects.create(name="BMW",
                                    country="Germany")

    def test_manufacturer_authenticated_user(self):
        self.client.login(username="testuser",
                          password="testpassword")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")

    def test_manufacturer_unauthenticated_user(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)


class DriverTestView(TestCase):
    def setUp(self):
        self.password = "testpassword"
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password=self.password
        )
        Driver.objects.create(
            username="alex_1993",
            first_name="Alex",
            last_name="Troianovskiy",
            email="test@gmail.com",
            license_number="ART12321",
        )

    def test_driver_authenticated_user(self):
        self.client.login(username="testuser", password=self.password)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "taxi/driver_list.html")

    def test_driver_unauthenticated_user(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)


class CarListViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        Car.objects.create(model="Corolla",
                           manufacturer=self.manufacturer)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             "/accounts/login/?next=/cars/")

    def test_view_if_logged_in(self):
        self.client.login(username="testuser",
                          password="testpassword")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "taxi/car_list.html")
