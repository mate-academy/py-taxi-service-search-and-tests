from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="admin123",
            license_number="ABC12345",
        )
        self.client.login(username="admin", password="admin123")


class DriverSearchViewTest(PrivateViewsTest):
    def setUp(self):
        super().setUp()
        Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="DEF12345",
        )
        Driver.objects.create_user(
            username="mike",
            password="12345",
            license_number="GHI12345",
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?q=john"
        )
        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")


class CarSearchViewTest(PrivateViewsTest):
    def setUp(self):
        super().setUp()
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?q=cor"
        )
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")


class ManufacturerSearchViewTest(PrivateViewsTest):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?q=au"
        )
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "BMW")


class PublicViewsTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)
