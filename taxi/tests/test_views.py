from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_manufacturer")
        Manufacturer.objects.create(name="test2_manufacturer")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {"name": "New Manufacturer", "country": "USA"}
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(manufacturer.name, form_data["name"])

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Old Manufacturer",
            country="USA"
        )
        form_data = {"name": "Updated Manufacturer", "country": "USA"}
        url = reverse("taxi:manufacturer-update", args=[manufacturer.id])
        self.client.post(url, data=form_data)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, form_data["name"])

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Delete Manufacturer")
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        self.client.post(url)
        self.assertFalse(Manufacturer.objects.filter(
            id=manufacturer.id).exists()
        )

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Ford")

        response = self.client.get(MANUFACTURER_URL, {"name": "Toy"})

        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.filter(name__icontains="Toy")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test firstname",
            "last_name": "Test lastname",
            "license_number": "TES12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_driver_detail(self):
        driver = get_user_model().objects.create_user(
            username="driver_user",
            password="test123",
            first_name="Driver",
            last_name="Test",
            license_number="DRI12345",
        )
        url = reverse("taxi:driver-detail", args=[driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, driver.first_name)
        self.assertContains(response, driver.last_name)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="driver_user",
            password="test123",
            license_number="DSI12345",
        )
        url = reverse("taxi:driver-delete", args=[driver.id])
        self.client.post(url)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="Toyota")

    def test_retrieve_cars(self):
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_create_car(self):
        form_data = {
            "model": "Yaris",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        car = Car.objects.get(model=form_data["model"])
        self.assertEqual(car.model, form_data["model"])
        self.assertEqual(car.manufacturer.id, self.manufacturer.id)

    def test_delete_car(self):
        car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        url = reverse("taxi:car-delete", args=[car.id])
        self.client.post(url)
        self.assertFalse(Car.objects.filter(id=car.id).exists())
