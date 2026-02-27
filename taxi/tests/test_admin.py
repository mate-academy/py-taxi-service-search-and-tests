from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car




class AdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver1234",
            password="testdriver",
            license_number="MIK25135"
        )
        self.manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        self.car = Car.objects.create(model="Camry", manufacturer=self.manufacturer)

    def test_driver_license_number_field_in_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_field_in_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_field_in_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "license_number")

    def test_car_model_search_field_in_add_search_fields(self):
        car1 = Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        car2 = Car.objects.create(model="Corolla", manufacturer=self.manufacturer)

        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"q": "Camry"})

        self.assertContains(res, car1.model)
        self.assertNotContains(res, car2.model)

    def test_car_list_filter_by_manufacturer(self):
        audi_manufacturer = Manufacturer.objects.create(name="Audi", country="Germany")
        Car.objects.create(model="Camry", manufacturer=audi_manufacturer)

        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertContains(res, "manufacturer")
        self.assertContains(res, self.manufacturer.name)


