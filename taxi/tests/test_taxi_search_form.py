from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchFormsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.test",
            email="admin@admin.com",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)

    def test_driver_username_search_form(self) -> None:
        for i in range(10):
            get_user_model().objects.create_user(
                username=f"test.{i}",
                first_name=f"TestName{i}",
                email="test@test.com",
                license_number=f"SSS1234{i}",
                password="testpassword123",

            )
        url = "%s?driver_username=test.5" % reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(
                get_user_model(
                ).objects.filter(username__istartswith="test.5")
            )
        )

    def test_manufacturer_name_search_form(self) -> None:
        for i in range(10):
            Manufacturer.objects.create(
                name=f"TestName{i}",
                country="TestCountry",
            )
        url = "%s?manufacturer_name=TestName2" % reverse(
            "taxi:manufacturer-list"
        )
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__istartswith="TestName2"))
        )

    def test_car_model_search_form(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry",
        )
        for i in range(10):
            Car.objects.create(
                model=f"TestName{i}",
                manufacturer=manufacturer,
            )
        url = "%s?car_model=TestName2" % reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__istartswith="TestName2"))
        )
