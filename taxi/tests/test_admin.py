from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class DriverAdminTests(TestCase):
    def setUp(self):
        self.admin_user = Driver.objects.create_superuser(
            username="test_admin",
            password="TestPassword123!",
            license_number="ADM12345",
        )
        self.client.force_login(self.admin_user)

        self.driver = Driver.objects.create_user(
            username="jim.hopper",
            first_name="Jim",
            last_name="Hopper",
            license_number="ABC12345",
        )

    def test_driver_list_displays_license_number(self):
        url = reverse("admin:taxi_driver_changelist")

        response = self.client.get(url)

        self.assertContains(response, "ABC12345")

    def test_driver_change_has_license_number(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        form = response.context["adminform"].form

        self.assertIn("license_number", form.fields)
        self.assertEqual(
            form.initial["license_number"],
            "ABC12345",
        )

    def test_driver_add_has_additional_fields(self):
        url = reverse("admin:taxi_driver_add")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        form = response.context["adminform"].form

        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("license_number", form.fields)


class CarAdminTests(TestCase):
    def setUp(self):
        self.admin_user = Driver.objects.create_superuser(
            username="test_admin",
            password="TestPassword123!",
            license_number="ADM12345",
        )
        self.client.force_login(self.admin_user)

        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.honda = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

        self.corolla = Car.objects.create(
            model="Corolla",
            manufacturer=self.toyota,
        )
        self.yaris = Car.objects.create(
            model="Yaris",
            manufacturer=self.toyota,
        )
        self.civic = Car.objects.create(
            model="Civic",
            manufacturer=self.honda,
        )

    def test_car_search_by_model(self):
        url = reverse("admin:taxi_car_changelist")

        response = self.client.get(url, {"q": "ORO"})

        self.assertEqual(response.status_code, 200)

        cars = response.context["cl"].result_list

        self.assertCountEqual(cars, [self.corolla])

    def test_car_search_without_matches(self):
        url = reverse("admin:taxi_car_changelist")

        response = self.client.get(
            url,
            {"q": "nonexistent-model"},
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["cl"].result_list

        self.assertCountEqual(cars, [])

    def test_car_filter_by_manufacturer(self):
        url = reverse("admin:taxi_car_changelist")

        response = self.client.get(
            url,
            {"manufacturer__id__exact": self.toyota.pk},
        )

        self.assertEqual(response.status_code, 200)

        changelist = response.context["cl"]

        self.assertTrue(changelist.has_filters)
        self.assertCountEqual(
            changelist.result_list,
            [self.corolla, self.yaris],
        )
