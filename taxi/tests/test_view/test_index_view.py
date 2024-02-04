from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")


class PublicIndexView(TestCase):
    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_num_visits(self):
        for visit in range(1, 10):
            res = self.client.get(INDEX_URL)
            self.assertEqual(res.context["num_visits"], visit)

    def test_index_context(self):
        for i in range(5):
            get_user_model().objects.create_user(
                username=f"test{i}",
                password="test123",
                license_number=f"AAA1234{i}"
            )
            manufacturer = Manufacturer.objects.create(
                name=f"Test_name{i}",
                country="Test_country"
            )
            Car.objects.create(
                manufacturer=manufacturer,
                model=f"Test_model{i}"
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(
            res.context["num_drivers"],
            get_user_model().objects.count()
        )
        self.assertEqual(
            res.context["num_manufacturers"],
            Manufacturer.objects.count()
        )
        self.assertEqual(
            res.context["num_cars"],
            Car.objects.count()
        )
