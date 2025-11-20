from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test_password",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

    def test_driver_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        self.assertContains(self.client.get(url), self.user.license_number)

    def test_driver_list_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        self.assertContains(self.client.get(url), self.user.license_number)

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        self.assertContains(self.client.get(url), 'name="license_number"')
        self.assertContains(self.client.get(url), 'name="first_name"')
        self.assertContains(self.client.get(url), 'name="last_name"')

    def test_car_search_fields(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test manufacturer country",
        )
        car_1 = Car.objects.create(
            model="Test Model 1",
            manufacturer=manufacturer,
        )
        car_2 = Car.objects.create(
            model="Test Model 2",
            manufacturer=manufacturer,
        )
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url, data={"q": "1"})
        self.assertContains(response, car_1.model)
        self.assertNotContains(response, car_2.model)

    def test_car_list_filter(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test manufacturer country",
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Test Manufacturer 2" ,
            country="Test manufacturer country",
        )
        Car.objects.create(
            model="Test Model 1",
            manufacturer=manufacturer_1,
        )
        car_2 = Car.objects.create(
            model="Test Model 2",
            manufacturer=manufacturer_2,
        )
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(
            url,
            data={"manufacturer__id__exact": manufacturer_2.id}
        )
        self.assertContains(response, car_2.model)
