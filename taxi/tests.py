from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

Driver = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin_user",
            password="pass12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.toyota = Manufacturer.objects.create(name="Toyota",
                                                  country="Japan")
        self.ford = Manufacturer.objects.create(name="Ford", country="USA")
        self.corolla = Car.objects.create(model="Corolla",
                                          manufacturer=self.toyota)
        self.mustang = Car.objects.create(model="Mustang",
                                          manufacturer=self.ford)


class SearchTests(BaseTestCase):
    def test_driver_search_includes_match_and_excludes_other(self):
        Driver.objects.create_user(
            username="john", password="pass12345", license_number="JOH12345"
        )
        res = self.client.get(reverse("taxi:driver-list"), {"username": "joh"})
        usernames = [d.username for d in res.context["driver_list"]]
        self.assertEqual(usernames, ["john"])
        self.assertNotIn("admin_user", usernames)

    def test_driver_search_is_case_insensitive(self):
        res = self.client.get(reverse("taxi:driver-list"),
                              {"username": "ADMIN"})
        self.assertEqual(len(res.context["driver_list"]), 1)

    def test_car_search_filters_by_model(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "must"})
        self.assertEqual(list(res.context["car_list"]), [self.mustang])

    def test_manufacturer_search_filters_by_name(self):
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              {"name": "toy"})
        self.assertEqual(list(res.context["manufacturer_list"]), [self.toyota])

    def test_search_without_matches_returns_empty_list(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "zzz"})
        self.assertEqual(len(res.context["car_list"]), 0)

    def test_empty_search_returns_all(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(len(res.context["car_list"]), 2)

    def test_search_form_keeps_value_in_context(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "must"})
        self.assertEqual(res.context["search_form"].initial["model"], "must")


class LoginRequiredTests(TestCase):
    def test_list_pages_redirect_anonymous_users(self):
        for name in ("driver-list", "car-list", "manufacturer-list"):
            res = self.client.get(reverse(f"taxi:{name}"))
            self.assertNotEqual(res.status_code, 200)
            self.assertEqual(res.status_code, 302)


class ModelTests(BaseTestCase):
    def test_manufacturer_str_contains_name(self):
        self.assertIn("Toyota", str(self.toyota))

    def test_car_str_contains_model(self):
        self.assertIn("Corolla", str(self.corolla))

    def test_driver_str_contains_username(self):
        self.assertIn("admin_user", str(self.user))

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.user.pk}),
        )


class CrudViewTests(BaseTestCase):
    def test_manufacturer_create(self):
        res = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Honda", "country": "Japan"},
        )
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_manufacturer_delete(self):
        res = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": self.ford.pk})
        )
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(pk=self.ford.pk).exists())


class PaginationSearchTests(BaseTestCase):
    def test_manufacturer_pagination_keeps_search_param(self):
        for i in range(6):
            Manufacturer.objects.create(name=f"Brand{i}", country="X")
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              {"name": "Brand"})
        self.assertContains(res, "page=2")
        self.assertContains(res, "name=Brand")

    def test_car_pagination_keeps_search_param(self):
        for i in range(6):
            Car.objects.create(model=f"Model{i}", manufacturer=self.toyota)
        res = self.client.get(reverse("taxi:car-list"), {"model": "Model"})
        self.assertContains(res, "page=2")
        self.assertContains(res, "model=Model")
