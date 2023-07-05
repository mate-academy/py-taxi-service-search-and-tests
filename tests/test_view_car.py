from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/cars/"
        )


class PrivateCarListTest(TestCase):
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
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )
