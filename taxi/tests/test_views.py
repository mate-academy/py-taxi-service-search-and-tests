from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from taxi.models import Car, Driver, Manufacturer
from taxi.templatetags.query_transform import query_transform

DRIVER_LIST = reverse("taxi:driver-list")
CAR_LIST = reverse("taxi:car-list")
MANUFACTURER_LIST = reverse("taxi:manufacturer-list")


class QueryTransformTagTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_add_new_param(self):
        """Добавление нового query параметра"""
        request = self.factory.get("/?page=1")
        result = query_transform(request, search="john")
        self.assertIn("page=1", result)
        self.assertIn("search=john", result)

    def test_update_existing_param(self):
        """Обновление существующего параметра"""
        request = self.factory.get("/?page=1")
        result = query_transform(request, page=2)
        self.assertEqual(result, "page=2")

    def test_remove_param_when_none(self):
        """Удаление параметра, если значение None"""
        request = self.factory.get("/?page=1&search=test")
        result = query_transform(request, search=None)
        # search удалён, остался только page
        self.assertEqual(result, "page=1")

    def test_multiple_changes(self):
        """Одновременное добавление и удаление"""
        request = self.factory.get("/?page=3&filter=active")
        result = query_transform(request, page=None, sort="name")
        # page удалён, filter остался, sort добавлен
        self.assertIn("filter=active", result)
        self.assertIn("sort=name", result)
        self.assertNotIn("page=", result)


class PrivateDriverFormat(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarFormat(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerFormat(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST)
        self.assertNotEqual(res.status_code, 200)


class CarListViewSearchTests(TestCase):
    def setUp(self):
        """Подготовка данных для теста"""
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Model X", manufacturer=manufacturer)
        Car.objects.create(model="Cybertruck", manufacturer=manufacturer)

        self.url = reverse("taxi:car-list")

    def test_search_returns_correct_results(self):
        """Поиск должен находить только подходящие машины"""
        response = self.client.get(self.url, {"model": "Model"})
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertEqual(cars.count(), 2)
        self.assertTrue(all("Model" in car.model for car in cars))

    def test_search_empty_returns_all(self):
        """Без параметра поиска должны вернуться все машины"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car_list"].count(), 3)


class DriverListViewSearchTests(TestCase):
    def setUp(self):
        """Создаём тестовых водителей"""
        self.user = get_user_model().objects.create_user(
            username="mainuser", password="password123"
        )
        self.client.login(username="mainuser", password="password123")

        Driver.objects.create(username="anton", license_number="A12345")
        Driver.objects.create(username="andrew", license_number="B67890")
        Driver.objects.create(username="peter", license_number="C11223")

        self.url = reverse("taxi:driver-list")

    def test_search_by_username(self):
        """Поиск должен фильтровать водителей по имени"""
        response = self.client.get(self.url, {"username": "an"})
        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        usernames = [d.username for d in drivers]
        self.assertIn("anton", usernames)
        self.assertIn("andrew", usernames)
        self.assertNotIn("peter", usernames)

    def test_search_empty_returns_all(self):
        """Без параметра поиска возвращаются все водители"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Driver.objects.count(), 4)


class ManufacturerListViewSearchTests(TestCase):
    def setUp(self):
        """Создаём тестовых производителей"""
        self.user = get_user_model().objects.create_user(
            username="tester", password="password123"
        )
        self.client.login(username="tester", password="password123")

        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        self.url = reverse("taxi:manufacturer-list")

    def test_search_by_name(self):
        """Поиск должен находить производителя по части имени"""
        response = self.client.get(self.url, {"name": "T"})
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        names = [m.name for m in manufacturers]
        self.assertIn("Tesla", names)
        self.assertIn("Toyota", names)
        self.assertNotIn("Ford", names)

    def test_search_empty_returns_all(self):
        """Без параметра поиска возвращаются все производители"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["manufacturer_list"].count(), 3)
