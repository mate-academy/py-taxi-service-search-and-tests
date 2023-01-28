from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewsTests(TestCase):

    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 302)


class PrivateViewsTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test_views",
            password="test password",
            license_number="RED12349",
        )
        self.client.force_login(self.user)

        for _ in range(1, 4):
            manufacturer = Manufacturer.objects.create(
                name=f"Name{_}", country=f"Country{_}"
            )
            Car.objects.create(
                model=f"model{_}",
                manufacturer=manufacturer
            )
            get_user_model().objects.create(
                username=f"test_driver{_}",
                password=f"test_driver_{_}_password",
                license_number=f"RED1234{_}"
            )

    def test_index_correct_objects_counting(self):
        response = self.client.get(reverse("taxi:index"))
        all_objects = {
            "manufacturers": Manufacturer.objects.count(),
            "drivers": get_user_model().objects.count(),
            "cars": Car.objects.count()
        }

        self.assertEqual(
            response.context["num_manufacturers"],
            all_objects["manufacturers"]
        )
        self.assertEqual(
            response.context["num_drivers"],
            all_objects["drivers"]
        )
        self.assertEqual(
            response.context["num_cars"],
            all_objects["cars"]
        )
        self.assertEqual(
            response.context["num_visits"],
            1
        )
