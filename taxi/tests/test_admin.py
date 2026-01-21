from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminPanelTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin1",
            password="passwordadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="passwordriver",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_change(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "license_number")
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_add(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "license_number")

    def test_car_search_field(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"q": "X5"})

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "X5")
        self.assertNotContains(res, "X4")

    def test_car_list_filter(self):
        manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        car1 = Car.objects.create(manufacturer=manufacturer1, model="X5")
        car2 = Car.objects.create(manufacturer=manufacturer2, model="X6")
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"manufacturer__id__exact": car1.id})

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, car1)
        self.assertNotContains(res, car2)
