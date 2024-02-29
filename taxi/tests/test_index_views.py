from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="i8",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_logged_in_response(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_records_counter(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(
            res.context["num_manufacturers"],
            Manufacturer.objects.all().count()
        )
        self.assertEqual(
            res.context["num_cars"],
            Car.objects.all().count()
        )
        self.assertEqual(
            res.context["num_drivers"],
            get_user_model().objects.all().count()
        )

    def test_visit_page_counter(self):
        for _ in range(5):
            self.client.get(INDEX_URL)
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.context["num_visits"], 6)
