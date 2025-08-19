from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

User = get_user_model()


class DriverSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.d1 = User.objects.create_user(
            username="studyuser", password="x", license_number="ABC12345"
        )
        cls.d2 = User.objects.create_user(
            username="studydev", password="x", license_number="DEF67890"
        )
        cls.d3 = User.objects.create_user(
            username="studymate", password="x", license_number="GHI54321"
        )

    def setUp(self):
        self.client.force_login(self.d1)

    def _url(self):
        return reverse("taxi:driver-list")

    def test_page_renders_and_has_form(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_form", resp.context)

    def test_form_keeps_typed_value(self):
        resp = self.client.get(self._url(), {"username": "study"})
        form = resp.context["search_form"]
        self.assertEqual(form["username"].value(), "study")

    def test_search_filters_by_username_icontains(self):
        resp = self.client.get(self._url(), {"username": "study"})
        usernames = [d.username for d in resp.context["object_list"]]
        self.assertCountEqual(
            usernames,
            ["studyuser", "studydev", "studymate"]
        )

    def test_empty_query_returns_all(self):
        resp = self.client.get(self._url())
        usernames = [d.username for d in resp.context["object_list"]]
        self.assertCountEqual(
            usernames,
            ["studyuser", "studydev", "studymate"]
        )

    def test_no_results(self):
        resp = self.client.get(self._url(), {"username": "mmm"})
        self.assertEqual(list(resp.context["object_list"]), [])


class CarSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        mercedes = Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        cls.car1 = Car.objects.create(model="Corolla", manufacturer=toyota)
        cls.car2 = Car.objects.create(model="C-Class", manufacturer=mercedes)
        cls.car3 = Car.objects.create(model="X5", manufacturer=bmw)
        cls.user = User.objects.create_user(
            username="studylogin", password="x", license_number="MNO11223"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def _url(self):
        return reverse("taxi:car-list")

    def test_page_renders_and_has_form(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_form", resp.context)

    def test_form_keeps_typed_value(self):
        resp = self.client.get(self._url(), {"model": "cor"})
        form = resp.context["search_form"]
        self.assertEqual(form["model"].value(), "cor")

    def test_search_filters_by_model_icontains(self):
        resp = self.client.get(self._url(), {"model": "class"})
        models = [c.model for c in resp.context["object_list"]]
        self.assertEqual(models, ["C-Class"])

    def test_empty_query_returns_all(self):
        resp = self.client.get(self._url())
        models = [c.model for c in resp.context["object_list"]]
        self.assertCountEqual(models, ["Corolla", "C-Class", "X5"])

    def test_no_results(self):
        resp = self.client.get(self._url(), {"model": "xxx"})
        self.assertEqual(list(resp.context["object_list"]), [])


class ManufacturerSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Mercedes-Benz", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

        cls.user = User.objects.create_user(
            username="studyuser", password="x", license_number="ABC12345"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def _url(self):
        return reverse("taxi:manufacturer-list")

    def test_page_renders_and_has_form(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_form", resp.context)

    def test_form_keeps_typed_value(self):
        resp = self.client.get(self._url(), {"name": "mercedes"})
        self.assertEqual(
            resp.context["search_form"]["name"].value(), "mercedes"
        )

    def test_search_filters_by_name_icontains(self):
        resp = self.client.get(self._url(), {"name": "mercedes"})
        names = [m.name for m in resp.context["object_list"]]
        self.assertEqual(names, ["Mercedes-Benz"])

    def test_empty_query_returns_all(self):
        resp = self.client.get(self._url())
        names = [m.name for m in resp.context["object_list"]]
        self.assertCountEqual(names, ["Toyota", "Mercedes-Benz", "BMW"])

    def test_no_results(self):
        resp = self.client.get(self._url(), {"name": "bbb"})
        self.assertEqual(list(resp.context["object_list"]), [])


class ManufacturerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m_audi = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        cls.m_bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        cls.m_merc = Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )
        cls.m_toy = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_str_returns_name_and_country(self):
        self.assertEqual(str(self.m_toy), "Toyota Japan")

    def test_ordering_by_name_meta(self):
        names = list(Manufacturer.objects.values_list("name", flat=True))
        self.assertEqual(names, ["Audi", "BMW", "Mercedes-Benz", "Toyota"])


class DriverModelTests(TestCase):
    def test_str_returns_username_and_full_name(self):
        user = User.objects.create_user(
            username="studyuser",
            password="x",
            first_name="Andrew",
            last_name="White",
            license_number="ABC00007",
        )
        self.assertEqual(str(user), "studyuser (Andrew White)")

    def test_get_absolute_url(self):
        user = User.objects.create_user(
            username="studydev",
            password="x",
            first_name="",
            last_name="",
            license_number="DEF67890",
        )
        self.assertEqual(
            user.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": user.pk})
        )


class CarModelTests(TestCase):
    def test_str_returns_model(self):
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        car = Car.objects.create(model="X5", manufacturer=bmw)
        self.assertEqual(str(car), "X5")

    def test_relations_fk_and_m2m(self):
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        car = Car.objects.create(model="Corolla", manufacturer=toyota)
        user1 = User.objects.create_user(
            username="study1", password="x", license_number="GHI54321"
        )
        user2 = User.objects.create_user(
            username="study2", password="x", license_number="JKL98765"
        )
        car.drivers.add(user1, user2)

        self.assertEqual(car.manufacturer.name, "Toyota")
        self.assertCountEqual(
            car.drivers.values_list(
                "username", flat=True
            ), ["study1", "study2"]
        )
