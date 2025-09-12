from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class BaseSetupMixin:
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()

        # users
        cls.user = cls.User.objects.create_user(
            username="john",
            password="pass12345",
            first_name="John",
            last_name="Doe",
            license_number="LIC001",
            email="john@example.com",
        )
        cls.other = cls.User.objects.create_user(
            username="jane",
            password="pass12345",
            first_name="Jane",
            last_name="Doe",
            license_number="LIC002",
            email="jane@example.com",
        )

        # manufacturers
        cls.m1 = Manufacturer.objects.create(name="Audi", country="Germany")
        cls.m2 = Manufacturer.objects.create(name="BMW", country="Germany")
        cls.m3 = Manufacturer.objects.create(name="ZAZ", country="Ukraine")

        # cars
        cls.c1 = Car.objects.create(model="A4", manufacturer=cls.m1)
        cls.c2 = Car.objects.create(model="X5", manufacturer=cls.m2)
        cls.c3 = Car.objects.create(model="Lanos", manufacturer=cls.m3)

        # relations
        cls.c1.drivers.add(cls.user)
        cls.c2.drivers.add(cls.user, cls.other)

    def login(self):
        self.client.force_login(self.user)


class AuthRequiredTests(BaseSetupMixin, TestCase):
    def test_all_views_require_login(self):
        protected = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=[self.m1.pk]),
            reverse("taxi:manufacturer-delete", args=[self.m1.pk]),
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", args=[self.c1.pk]),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", args=[self.c1.pk]),
            reverse("taxi:car-delete", args=[self.c1.pk]),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", args=[self.user.pk]),
            reverse("taxi:driver-create"),
            reverse("taxi:toggle-car-assign", args=[self.c1.pk]),
        ]
        for url in protected:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 302)
                self.assertIn("/accounts/login/", resp["Location"])


class IndexViewTests(BaseSetupMixin, TestCase):
    def test_index_counts_and_session_visits(self):
        self.login()
        url = reverse("taxi:index")

        # перший візит
        resp1 = self.client.get(url)
        self.assertEqual(resp1.status_code, 200)

        # перевіряємо контекст
        self.assertEqual(
            resp1.context["num_drivers"],
            self.User.objects.count()
        )
        self.assertEqual(
            resp1.context["num_cars"],
            Car.objects.count()
        )
        self.assertEqual(
            resp1.context["num_manufacturers"],
            Manufacturer.objects.count()
        )
        self.assertEqual(
            resp1.context["num_visits"],
            1
        )

        # (необов’язково) перевірити, що числа вивелись у HTML
        self.assertContains(resp1, "<strong>Cars:</strong> 3")
        self.assertContains(resp1, "<strong>Drivers:</strong> 2")
        self.assertContains(resp1, "<strong>Manufacturers:</strong> 3")

        # другий візит інкрементить лічильник
        resp2 = self.client.get(url)
        self.assertEqual(resp2.context["num_visits"], 2)


class ManufacturerViewsTests(BaseSetupMixin, TestCase):
    def setUp(self):
        self.login()

    def test_list_default(self):
        url = reverse("taxi:manufacturer-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        expected = list(Manufacturer.objects.order_by("name"))
        actual = list(resp.context["manufacturer_list"])
        self.assertEqual(expected, actual)
        self.assertIn("search_manufacturer_form", resp.context)

    def test_list_search(self):
        url = reverse("taxi:manufacturer-list")
        resp = self.client.get(url, {"title": "a"})  # Audi, ZAZ
        self.assertEqual(resp.status_code, 200)
        names = [m.name for m in resp.context["manufacturer_list"]]
        self.assertIn("Audi", names)
        self.assertIn("ZAZ", names)
        self.assertNotIn("BMW", names)

    def test_create(self):
        url = reverse("taxi:manufacturer-create")
        data = {"name": "Toyota", "country": "Japan"}
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Manufacturer.objects.filter(name="Toyota").exists())

    def test_update(self):
        url = reverse("taxi:manufacturer-update", args=[self.m1.pk])
        resp = self.client.post(
            url,
            {"name": "Audi AG", "country": "Germany"},
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.m1.refresh_from_db()
        self.assertEqual(self.m1.name, "Audi AG")

    def test_delete(self):
        url = reverse("taxi:manufacturer-delete", args=[self.m2.pk])
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Manufacturer.objects.filter(pk=self.m2.pk).exists())


class CarViewsTests(BaseSetupMixin, TestCase):
    def setUp(self):
        self.login()

    def test_list_default(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_car_form", resp.context)
        # просто переконаємось, що повертається хоч щось з фікстур
        returned_models = {c.model for c in resp.context["car_list"]}
        self.assertTrue({"A4", "X5", "Lanos"}.issubset(returned_models))

    def test_list_search(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"title": "x"})
        self.assertEqual(resp.status_code, 200)
        models = [c.model.lower() for c in resp.context["car_list"]]
        self.assertIn("x5", models)
        self.assertNotIn("a4", models)

    def test_detail(self):
        url = reverse("taxi:car-detail", args=[self.c1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        car = resp.context["car"]
        self.assertEqual(car.model, "A4")
        # виробник доступний (select_related у в’ю)
        self.assertEqual(car.manufacturer.name, "Audi")

    def test_create(self):
        url = reverse("taxi:car-create")
        data = {
            "model": "Corolla",
            "manufacturer": self.m3.pk,
            "drivers": [self.user.pk, self.other.pk],
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Car.objects.filter(model="Corolla").exists())
        car = Car.objects.get(model="Corolla")
        self.assertEqual(car.manufacturer, self.m3)
        self.assertEqual(
            set(car.drivers.values_list("pk", flat=True)),
            {self.user.pk, self.other.pk}
        )

    def test_update(self):
        url = reverse("taxi:car-update", args=[self.c3.pk])
        data = {
            "model": "Lanos SE",
            "manufacturer": self.m3.pk,
            "drivers": [self.user.pk],
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.c3.refresh_from_db()
        self.assertEqual(self.c3.model, "Lanos SE")
        self.assertEqual(
            list(self.c3.drivers.values_list("pk", flat=True)),
            [self.user.pk]
        )

    def test_delete(self):
        url = reverse("taxi:car-delete", args=[self.c2.pk])
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Car.objects.filter(pk=self.c2.pk).exists())

    def test_toggle_assign(self):
        self.assertIn(self.c1, self.user.cars.all())
        url = reverse("taxi:toggle-car-assign", args=[self.c1.pk])
        resp = self.client.post(url, follow=False)
        # редірект на detail
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp["Location"],
            reverse("taxi:car-detail", args=[self.c1.pk])
        )
        # тепер відв’язаний
        self.user.refresh_from_db()
        self.assertNotIn(self.c1, self.user.cars.all())

        # ще раз — має знову прив’язати
        resp2 = self.client.post(url, follow=False)
        self.assertEqual(resp2.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.c1, self.user.cars.all())


class DriverViewsTests(BaseSetupMixin, TestCase):
    def setUp(self):
        self.login()

    def test_list_default(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_driver_form", resp.context)
        usernames = {u.username for u in resp.context["driver_list"]}
        self.assertTrue({"john", "jane"}.issubset(usernames))

    def test_list_search(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url, {"title": "jan"})
        self.assertEqual(resp.status_code, 200)
        usernames = [u.username for u in resp.context["driver_list"]]
        self.assertIn("jane", usernames)
        self.assertNotIn("john", usernames)

    def test_detail_with_prefetched_cars(self):
        url = reverse("taxi:driver-detail", args=[self.user.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        driver = resp.context["driver"]
        # у контексті є машини користувача
        car_models = {c.model for c in driver.cars.all()}
        self.assertTrue({"A4", "X5"}.issubset(car_models))

    def test_driver_create_view_get(self):
        url = reverse("taxi:driver-create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)

    def test_driver_license_update(self):
        url = reverse("taxi:driver-update", args=[self.user.pk])
        resp = self.client.post(
            url,
            {"license_number": "LIC77744"},
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "LIC77744")
