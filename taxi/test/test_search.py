from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

User = get_user_model()


class SearchIntegrationTests(TestCase):
    def setUp(self):
        self.password = "pass12345"
        self.user = User.objects.create_user(
            username="tester",
            password=self.password,
            license_number="DRV00001",
        )
        self.client = Client()
        self.client.login(username=self.user.username, password=self.password)

        self.m1 = Manufacturer.objects.create(name="Lincoln", country="USA")
        self.m2 = Manufacturer.objects.create(
            name="Mitsubishi", country="Japan"
        )

        self.c1 = Car.objects.create(model="Navigator", manufacturer=self.m1)
        self.c2 = Car.objects.create(model="L200", manufacturer=self.m2)

        User.objects.create_user(
            username="linus", password="x", license_number="DRV00002"
        )
        User.objects.create_user(
            username="alice", password="x", license_number="DRV00003"
        )

    def test_empty_query_returns_all(self):
        resp = self.client.get(reverse("taxi:driver-list"), {"username": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.context["paginator"].count, 3)

        resp = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["paginator"].count, 2)

        resp = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["paginator"].count, 2)

    def test_whitespace_query_behaves_like_empty(self):
        resp = self.client.get(
            reverse("taxi:driver-list"), {"username": "   "}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.context["paginator"].count, 3)

        resp = self.client.get(reverse("taxi:car-list"), {"model": "   "})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["paginator"].count, 2)

        resp = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "   "}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["paginator"].count, 2)

    def test_search_filters_results(self):
        resp = self.client.get(
            reverse("taxi:driver-list"), {"username": "lin"}
        )
        self.assertEqual(resp.status_code, 200)
        usernames = [u.username for u in resp.context["driver_list"]]
        self.assertIn("linus", usernames)
        self.assertNotIn("alice", usernames)
        self.assertEqual(
            resp.context["search_form"]["username"].value(), "lin"
        )

        resp = self.client.get(reverse("taxi:car-list"), {"model": "nav"})
        self.assertEqual(resp.status_code, 200)
        models = [c.model for c in resp.context["car_list"]]
        self.assertIn("Navigator", models)
        self.assertNotIn("L200", models)
        self.assertEqual(resp.context["search_form"]["model"].value(), "nav")

        resp = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "mit"}
        )
        self.assertEqual(resp.status_code, 200)
        names = [m.name for m in resp.context["manufacturer_list"]]
        self.assertIn("Mitsubishi", names)
        self.assertNotIn("Lincoln", names)
        self.assertEqual(resp.context["search_form"]["name"].value(), "mit")

    def test_pagination_with_search_param(self):
        for i in range(10):
            Manufacturer.objects.create(name=f"M{i} test", country="X")

        url = reverse("taxi:manufacturer-list")
        resp = self.client.get(url, {"page": 2, "name": "test"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["page_obj"].number, 2)
        for obj in resp.context["manufacturer_list"]:
            self.assertIn("test", obj.name.lower())
