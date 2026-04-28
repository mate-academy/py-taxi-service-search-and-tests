from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer, Driver


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )

        # Создаем данные для теста
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")

    def test_search_manufacturer_by_name(self):
        # Логиним пользователя в тестовом клиенте
        self.client.force_login(self.user)

        url = reverse("taxi:manufacturer-list")
        # Проверяем поиск, который должен вернуть результат
        response = self.client.get(url, {"name": "toyota"})

        # Теперь статус должен быть 200
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")


class SearchFeatureTests(TestCase):
    def setUp(self):
        # Создаем производителя для машин
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        # Создаем машины для теста поиска
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Prius",
            manufacturer=self.manufacturer
        )

        # Создаем водителей для теста поиска
        self.driver1 = get_user_model().objects.create_user(
            username="jdoe",
            password="password123",
            license_number="AAA11111",  # Уникальный номер
        )
        self.driver2 = get_user_model().objects.create_user(
            username="micheal",
            password="password123",
            license_number="BBB22222",  # Уникальный номер
        )

        # АВТОРИЗАЦИЯ:
        # теперь клиент "залогинен" для всех тестов в этом классе
        self.client.force_login(self.driver1)
        self.client.force_login(self.driver2)

    # --- Тесты для Cars ---

    def test_car_search_by_model_exists(self):
        url = reverse("taxi:car-list")

        # Если нет авторизации в force_login в setUp:
        self.client.login(username="test.user", password="password123")

        # Ищем "Co" — должна найтись Corolla
        response = self.client.get(url, {"model": "Co"})

        # Должен вернуть 200
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_car_search_case_insensitive(self):
        url = reverse("taxi:car-list")
        # Проверяем, что поиск регистронезависимый (icontains)
        response = self.client.get(url, {"model": "pRiUs"})

        self.assertContains(response, "Prius")

    # --- Тесты для Drivers ---
    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")

        # Логиним пользователя перед запросом
        # Мы используем driver1, созданного в setUp
        self.client.force_login(self.driver1)
        # Запрос должен вернуть 200 OK
        response = self.client.get(url, {"username": "jdoe"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_driver_search_empty_result(self):
        url = reverse("taxi:driver-list")
        # Логинимся перед запросом
        self.client.force_login(self.driver1)

        # Ищем того, кого нет
        response = self.client.get(url, {"username": "non_existent_user"})

        # Проверяем, что страница вообще загрузилась
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в списке объектов (в контексте) пусто
        # чтобы избежать ошибки, если ключа нет,
        # или проверяем через object_list
        drivers = response.context.get(
            "driver_list"
        )  # or response.context.get("object_list")

        self.assertIsNotNone(drivers, "Контекст не содержит список водителей")
        self.assertEqual(len(drivers), 0)
