from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class DriverModelTest(TestCase):
    def test_str_method(self):
        driver = Driver(username="luke", first_name="Luke",
                        last_name="Skywalker")
        self.assertEqual(str(driver), "luke (Luke Skywalker)")

    def test_search_driver(self):
        # Adicione license_number único para evitar erro de unicidade
        Driver.objects.create_user(username="luke",
                                   password="test123",
                                   license_number="ABC12345")
        Driver.objects.create_user(username="anna",
                                   password="test123",
                                   license_number="DEF12345")
        # Faz login antes de acessar a página
        self.client.login(username="luke", password="test123")

        response = self.client.get("/drivers/?username=luke")
        self.assertContains(response, "luke")
        self.assertNotContains(response, "anna")


class CarModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer(name="Toyota")
        car = Car(manufacturer=manufacturer, model="Corolla")
        self.assertEqual(str(car), "Corolla")

    def test_car_manufacturer_relationship(self):
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        car = Car.objects.create(model="Corolla",
                                 manufacturer=manufacturer)
        self.assertEqual(car.manufacturer.name, "Toyota")

    def test_car_drivers_relationship(self):
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        car = Car.objects.create(model="Corolla",
                                 manufacturer=manufacturer)
        driver = Driver.objects.create_user(username="luke",
                                            password="test123",
                                            license_number="ABC12345")
        car.drivers.add(driver)
        self.assertIn(driver, car.drivers.all())


class ManufacturerModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer(name="Ford", country="USA")
        self.assertEqual(str(manufacturer), "Ford USA")


class SearchTest(TestCase):
    def setUp(self):
        # Cria usuário para login nos testes
        self.user = User.objects.create_user(username="testuser",
                                             password="test123",
                                             license_number="TEST12345")
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.driver = Driver.objects.create_user(username="luke",
                                                 password="test123",
                                                 license_number="ABC12345")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)

    def test_driver_search(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?username=luke")
        self.assertContains(response, "luke")

    def test_driver_search_no_results(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?username=nonexistent")
        self.assertNotContains(response, "luke")

    def test_car_search(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("taxi:car-list")
                                   + "?model=Corolla")
        self.assertContains(response, "Corolla")

    def test_manufacturer_search(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=Toyota")
        self.assertContains(response, "Toyota")
