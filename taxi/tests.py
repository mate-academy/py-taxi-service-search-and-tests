from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth import get_user_model


class SearchFeatureTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестовых данных для поиска
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        cls.driver1 = Driver.objects.create_user(
            username="john_doe",
            password="testpass123",
            license_number="ABC12345"
        )
        cls.driver2 = Driver.objects.create_user(
            username="jane_smith",
            password="testpass123",
            license_number="XYZ67890"
        )
        cls.car1 = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer1
        )
        cls.car2 = Car.objects.create(
            model="Focus",
            manufacturer=cls.manufacturer2
        )

    def setUp(self):
        # Логиним пользователя для всех тестов
        self.client.login(username="john_doe", password="testpass123")

    def test_search_manufacturers(self):
        # Поиск по существующему производителю
        response = self.client.get(
            reverse(
                "taxi:manufacturer-list"),
            {"search": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_drivers(self):
        # Поиск по существующему водителю
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john_doe"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")

    def test_search_cars(self):
        # Поиск по модели автомобиля
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Focus")


class CRUDTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        cls.driver = Driver.objects.create_user(
            username="john_doe",
            password="testpass123",
            license_number="ABC12345"
        )
        cls.car = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer
        )

    def setUp(self):
        # Логиним пользователя для всех тестов
        self.client.login(username="john_doe", password="testpass123")

    def test_create_car(self):
        # Попытка создания машины с обязательными данными, включая водителей
        response = self.client.post(reverse("taxi:car-create"), {
            "model": "Civic",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        })

        # Выводим ошибки формы для диагностики
        if response.context and "form" in response.context:
            print(response.context["form"].errors)

        # Ожидаем успешного редиректа
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Civic").exists())

    def test_update_car(self):
        response = self.client.post(
            reverse("taxi:car-update", args=[self.car.id]),
            {
                "model": "Camry Updated",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.driver.id]
            }
        )

        # Выводим ошибки формы для диагностики
        if response.context and "form" in response.context:
            print(response.context["form"].errors)

        # Ожидаем успешного редиректа
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Camry Updated")
