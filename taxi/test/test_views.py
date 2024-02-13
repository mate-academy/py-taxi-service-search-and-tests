from django.test import TestCase
from django.urls import reverse


class AccessTest(TestCase):
    def setUp(self):
        self.urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:car-list"),
            reverse("taxi:car-create"),
            reverse("taxi:car-detail", kwargs={"pk": 1}),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-detail", kwargs={"pk": 1}),
        ]

    def test_login_required_mixin(self):
        for url in self.urls:
            self.assertNotEqual(self.client.get(url).status_code, 200)
