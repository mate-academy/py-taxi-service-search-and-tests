from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth.hashers import make_password


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        password = make_password("password")
        self.user = Driver.objects.create(
            username="testuser", password=password
        )
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class DriverDetailViewTest(TestCase):
    def setUp(self):
        password = make_password("password")
        self.user = Driver.objects.create(
            username="testuser",
            password=password,
            first_name="John",
            last_name="Doe",
            license_number="JDO12345",
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get(f"/drivers/{self.user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class CarListViewTest(TestCase):
    def setUp(self):
        password = make_password("password")
        self.user = Driver.objects.create(
            username="testuser", password=password
        )
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
