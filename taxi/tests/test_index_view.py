from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.tests import fixtures

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTests(TestCase):
    def test_login_required_and_redirect_if_not_authenticated(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next=/')


class PrivateIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def setUp(self):
        self.user = get_user_model().objects.get(id=1)
        self.client.force_login(self.user)

    def test_should_use_defined_template(self):
        self.assertTemplateUsed(self.client.get(INDEX_URL), "taxi/index.html")

    def test_context_contains_correct_data(self):
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context.get("num_drivers"), fixtures.DRIVERS_AMOUNT
        )
        self.assertEqual(
            response.context.get("num_cars"), fixtures.CARS_AMOUNT
        )
        self.assertEqual(
            response.context.get("num_manufacturers"),
            fixtures.MANUFACTURERS_AMOUNT
        )

    def test_num_visits_counter_increase_after_visit(self):
        self.client.get(INDEX_URL)
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.context.get("num_visits"), 2)
