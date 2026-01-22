from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

Driver = get_user_model()


class IndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.URL = reverse("taxi:index")
        cls.drivers_count = 3
        cls.cars_count = 5
        cls.manufacturers_count = 10

        for driver_copy in range(cls.drivers_count):
            Driver.objects.create_user(
                username=f"Username {driver_copy}",
                password="test_password",
                license_number=f"AAA1234{driver_copy}"
            )

        for manufacturer_copy in range(cls.manufacturers_count):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_copy}",
                country=f"Country {manufacturer_copy}",
            )

        for cars_copy in range(cls.cars_count):
            Car.objects.create(
                model=f"Car {cars_copy}",
                manufacturer=Manufacturer.objects.get(
                    pk=cars_copy / cls.manufacturers_count + 1
                ),
            )

    def test_login_required(self):
        response = self.client.get(IndexTest.URL)
        self.assertRedirects(
            response,
            reverse("login") + f"?next={IndexTest.URL}"
        )

    def test_use_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(IndexTest.URL)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_nums_of_objects_in_context(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(IndexTest.URL)

        self.assertEqual(
            response.context["num_drivers"],
            Driver.objects.count()
        )

        self.assertEqual(
            response.context["num_cars"],
            Car.objects.count()
        )

        self.assertEqual(
            response.context["num_manufacturers"],
            Manufacturer.objects.count()
        )

    def test_num_visits(self):
        self.client.force_login(Driver.objects.get(pk=1))

        for visit in range(1, 10):
            response = self.client.get(IndexTest.URL)

            self.assertEqual(response.context["num_visits"], visit)

        self.client.logout()
        self.client.force_login(Driver.objects.get(pk=1))

        response = self.client.get(IndexTest.URL)
        self.assertEqual(response.context["num_visits"], 1)
