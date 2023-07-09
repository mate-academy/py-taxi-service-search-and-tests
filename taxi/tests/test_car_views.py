from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarViewTest(TestCase):
    def test_login_required_driver_list(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(res, "/accounts/login/?next=/cars/")


class PrivateCarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )
        for car_id in range(8):
            Car.objects.create(
                model=f"Test Model-{car_id}",
                manufacturer=manufacturer
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/cars/")

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_correct_pagination_on_first_page(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["car_list"]), 5)

    def test_correct_pagination_on_second_page(self):
        response = self.client.get(CAR_LIST_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["car_list"]), 3)
