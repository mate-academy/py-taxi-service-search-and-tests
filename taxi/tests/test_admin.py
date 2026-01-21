from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminTest(TestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="TestAdmin", password="TestPassword"
        )
        self.client.force_login(self.admin_user)

    def test_driver_license_list_display(self):
        get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="TES32288",
        )
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, "License number")
        self.assertContains(response, "TES32288")

    def test_driver_additional_info_change_display(self):
        user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            first_name="TestFirstName",
            license_number="TES32288",
        )
        url = reverse("admin:taxi_driver_change", args=[user.id])
        response = self.client.get(url)
        self.assertContains(response, "Additional info")
        self.assertContains(response, "TestFirstName")

    def test_driver_additional_info_add_display(self):
        get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            first_name="TestFirstName",
            license_number="TES32288",
        )
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "Additional info")
        self.assertContains(response, "License number")

    def test_car_search_by_model(self):
        mn = Manufacturer.objects.create(name="TEST", country="TEST")
        Car.objects.create(model="987552", manufacturer=mn)
        Car.objects.create(model="334567", manufacturer=mn)
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url, data={"q": "987"})
        self.assertContains(response, "552")
        self.assertNotContains(response, "334567")

    def test_car_list_filter_by_manufacturer(self):
        mn = Manufacturer.objects.create(name="TEST", country="TEST")
        mn_two = Manufacturer.objects.create(name="TEST2", country="TEST")
        Car.objects.create(model="888777", manufacturer=mn)
        Car.objects.create(model="767565", manufacturer=mn_two)
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(
            url, data={"manufacturer__id__exact": mn.pk}
        )
        self.assertContains(response, "888777")
        self.assertNotContains(response, "767565")
