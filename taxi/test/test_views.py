from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car

User = get_user_model()


class BaseAuthTestCase(TestCase):
    def setUp(self):
        self.password = "pass12345"
        self.user = User.objects.create_user(
            username="tester", password=self.password
        )
        self.client = Client()
        self.client.login(username=self.user.username, password=self.password)


class IndexViewTests(BaseAuthTestCase):
    def test_index_requires_login(self):
        self.client.logout()
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_index_ok_and_context(self):
        Manufacturer.objects.create(name="M1", country="UA")
        Car.objects.create(
            model="X",
            manufacturer=Manufacturer.objects.create(name="M2", country="PL"),
        )
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_manufacturers", response.context)


class DriverListViewTests(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        User.objects.create_user(username="anna", password="q")
        User.objects.create_user(username="Annabel", password="q")
        User.objects.create_user(username="bob", password="q")


class ManufacturerListViewTests(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="Ford Motor Company", country="USA")
        Manufacturer.objects.create(name="General Motors", country="USA")
        Manufacturer.objects.create(name="Mitsubishi", country="Japan")

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)

    def test_context_contains_search_form(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

    def test_search_by_name_icontains(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "mot"})
        self.assertEqual(response.status_code, 200)
        names = [m.name for m in response.context["manufacturer_list"]]
        self.assertIn("Ford Motor Company", names)
        self.assertIn("General Motors", names)
        self.assertNotIn("Mitsubishi", names)
        self.assertEqual(
            response.context["search_form"]["name"].value(), "mot"
        )


class CarListViewTests(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        m1 = Manufacturer.objects.create(name="Ford", country="USA")
        m2 = Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Focus", manufacturer=m1)
        Car.objects.create(model="Fiesta", manufacturer=m1)
        Car.objects.create(model="Corolla", manufacturer=m2)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_context_contains_search_form(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)

    def test_search_by_model_icontains(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "fi"})
        self.assertEqual(response.status_code, 200)
        models = [c.model for c in response.context["car_list"]]
        self.assertIn("Fiesta", models)
        self.assertNotIn("Focus", models)
        self.assertNotIn("Corolla", models)
        self.assertEqual(
            response.context["search_form"]["model"].value(), "fi"
        )


class ToggleAssignToCarViewTests(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        self.car = Car.objects.create(
            model="Focus", manufacturer=self.manufacturer
        )

    def test_toggle_add_and_remove(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.cars.filter(id=self.car.id).exists())
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.cars.filter(id=self.car.id).exists())
