from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


CAR_FORMAT_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        """
        Checking possibility for non-login user have access to Car-list
        working LoginRequiredMixin for CarListView
        :return:
        """
        res = self.client.get(CAR_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarFormat(TestCase):
    def setUp(self) -> None:
        number_of_cars = 7

        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test12345",
            first_name="test_first1",
            last_name="test_last1",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Audi_test",
            country="Germany_test",
        )

        for car_id in range(number_of_cars):
            car = Car.objects.create(
                model=f"Test-name {car_id}",
                manufacturer=manufacturer,
            )
            car.drivers.add(self.user)

    def test_retrieve_car_formats(self):
        """
        Checking access login user to CarListView page
        """
        response = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        car_formats = Car.objects.all()[:5]
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_formats),
        )
        # checking url path to taxi/car_list.html
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_car_is_five(self):
        response = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_all_cars(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(CAR_FORMAT_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 2)
