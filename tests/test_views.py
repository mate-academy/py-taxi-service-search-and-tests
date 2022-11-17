from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

URLS = {
    "HOMEPAGE_URL": reverse("taxi:index"),
    "MANUFACTURER_LIST_URL": reverse("taxi:manufacturer-list"),
    "CAR_LIST_URL": reverse("taxi:car-list"),
    "DRIVER_LIST_URL": reverse("taxi:driver-list"),
}


class PublicViewsTests(TestCase):
    def test_login_required(self):
        for url in URLS.values():
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_pass_12345",
        )
        self.client.force_login(self.user)

    # imho, rest of the list views will be logically equivalent
    def test_retrieve_manufacturers_list(self):
        Manufacturer.objects.create(name="test_1", country="some_country")
        Manufacturer.objects.create(name="test_2", country="not_that_country")

        resp = self.client.get(URLS["MANUFACTURER_LIST_URL"])
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_retrieve_with_search_form(self):
        resp = self.client.get("/manufacturers/?name=Zaporozhets")

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(
            resp.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="zaporozhets")
        )
