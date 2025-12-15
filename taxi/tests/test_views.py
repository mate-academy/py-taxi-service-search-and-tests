from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

HOME_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicPagesTest(TestCase):
    def test_login_required_home(self):
        response_home = self.client.get(HOME_URL)

        self.assertNotEqual(response_home.status_code, 200)

    def test_login_required_manufacturer(self):
        response_manufacturer = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response_manufacturer.status_code, 200)

    def test_login_required_driver(self):
        response_driver = self.client.get(DRIVER_URL)

        self.assertNotEqual(response_driver.status_code, 200)

    def test_login_required_car(self):
        response_car = self.client.get(CAR_URL)

        self.assertNotEqual(response_car.status_code, 200)

    def test_login_required_driver_detail(self):
        get_user_model().objects.create_user(
            username="test",
            password="test"
        )
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_detail(self):
        Manufacturer.objects.create(
            name="ttt",
            country="www"
        )
        Car.objects.create(
            model="test",
            manufacturer_id=1
        )
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateAllPagesTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="MrCrabs",
            password="SecretFormula",
            license_number="TBS45670"
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="SpongeBob",
            password="CrabsBurger",
            license_number="TBS45678"
        )
        get_user_model().objects.create_user(
            username="Patric",
            password="WhatIsPassword",
            license_number="FRB45678"
        )
        Manufacturer.objects.create(
            name="Uncle_Bob",
            country="Bob_land"
        )
        Manufacturer.objects.create(
            name="Sponge_service",
            country="Bikini_Bottom"
        )
        Car.objects.create(
            model="Rock",
            manufacturer_id=1
        )
        Car.objects.create(
            model="Garry",
            manufacturer_id=2
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_retrieve_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"].username, "MrCrabs")

    def test_retrieve_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"].model, "Rock")

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "Uncle_Bob"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uncle_Bob")
        self.assertContains(response, "Bob_land")
        self.assertContains(response, 1)
        self.assertNotContains(response, "Sponge_service")

    def test_driver_search(self):
        response = self.client.get(DRIVER_URL, {"username": "SpongeBob"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SpongeBob")
        self.assertContains(response, 2)
        self.assertNotContains(response, "SecretFormula")
        self.assertNotContains(response, "Patric")

    def test_car_search(self):
        response = self.client.get(CAR_URL, {"model": "Rock"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rock")
        self.assertContains(response, 1)
        self.assertContains(response, "Uncle_Bob")
        self.assertNotContains(response, "Garry")

    def test_manufacturer_create(self):
        new_manufacturer_data = {
            "name": "Tesla",
            "country": "USA"
        }

        initial_count = Manufacturer.objects.count()

        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=new_manufacturer_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_URL)

        self.assertEqual(Manufacturer.objects.count(), initial_count + 1)

        new_manufacturer = Manufacturer.objects.get(name="Tesla")
        self.assertEqual(new_manufacturer.country, "USA")

    def test_driver_create(self):
        new_driver_data = {
            "username": "Admin",
            "password1": "QWE45678",
            "password2": "QWE45678",
            "license_number": "QWE45678",
            "first_name": "Test",
            "last_name": "NewDriver",
        }

        initial_count = get_user_model().objects.count()

        response = self.client.post(
            reverse("taxi:driver-create"),
            data=new_driver_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), initial_count + 1)

        new_driver = get_user_model().objects.get(username="Admin")
        self.assertEqual(new_driver.license_number, "QWE45678")

    def test_car_create(self):
        manufacturer_pk = 1
        drivers_pks = [1, 2]

        new_car_data = {
            "model": "New_Car_Test_Model",
            "manufacturer": manufacturer_pk,
            "drivers": drivers_pks,
        }

        initial_count = Car.objects.count()

        response = self.client.post(
            reverse("taxi:car-create"),
            data=new_car_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), initial_count + 1)

        new_car = Car.objects.get(model="New_Car_Test_Model")

        self.assertEqual(new_car.model, "New_Car_Test_Model")
        self.assertEqual(new_car.manufacturer.pk, manufacturer_pk)
        self.assertEqual(new_car.drivers.count(), len(drivers_pks))

    def test_manufacturer_update(self):
        manufacturer_to_update = Manufacturer.objects.get(name="Uncle_Bob")

        updated_data = {
            "name": "Uncle_Bob_Updated",
            "country": "Atlantis"
        }

        update_url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": manufacturer_to_update.pk}
        )

        response = self.client.post(update_url, data=updated_data)
        manufacturer_to_update.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_URL)

        self.assertEqual(manufacturer_to_update.name, "Uncle_Bob_Updated")
        self.assertEqual(manufacturer_to_update.country, "Atlantis")

        self.assertEqual(Manufacturer.objects.count(), 2)

    def test_driver_update(self):
        driver_to_update = get_user_model().objects.get(username="SpongeBob")

        updated_data = {
            "license_number": "ZXC00000"
        }

        update_url = reverse(
            "taxi:driver-update",
            kwargs={"pk": driver_to_update.pk}
        )

        response = self.client.post(update_url, data=updated_data)
        driver_to_update.refresh_from_db()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(driver_to_update.license_number, "ZXC00000")

        self.assertEqual(get_user_model().objects.count(), 3)

    def test_car_update(self):
        car_to_update = Car.objects.get(model="Rock")

        driver_for_car = get_user_model().objects.get(username="Patric")
        car_to_update.drivers.add(driver_for_car)

        current_drivers_pks = list(
            car_to_update.drivers.values_list("pk", flat=True)
        )

        updated_data = {
            "model": "Rock_updated",
            "manufacturer": car_to_update.manufacturer.pk,
            "drivers": current_drivers_pks,
        }

        update_url = reverse(
            "taxi:car-update",
            kwargs={"pk": car_to_update.pk}
        )

        response = self.client.post(update_url, data=updated_data)
        car_to_update.refresh_from_db()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(car_to_update.model, "Rock_updated")

        self.assertEqual(car_to_update.manufacturer.name, "Uncle_Bob")
        self.assertEqual(
            car_to_update.drivers.count(),
            len(current_drivers_pks)
        )

        self.assertEqual(Car.objects.count(), 2)

    def test_manufacturer_delete(self):
        manufacturer_to_delete = Manufacturer.objects.get(
            name="Sponge_service"
        )

        initial_count = Manufacturer.objects.count()

        delete_url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": manufacturer_to_delete.pk}
        )

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_URL)

        self.assertEqual(Manufacturer.objects.count(), initial_count - 1)

        with self.assertRaises(Manufacturer.DoesNotExist):
            Manufacturer.objects.get(pk=manufacturer_to_delete.pk)

    def test_driver_delete(self):
        driver_to_delete = get_user_model().objects.get(username="SpongeBob")

        initial_count = get_user_model().objects.count()

        delete_url = reverse(
            "taxi:driver-delete",
            kwargs={"pk": driver_to_delete.pk}
        )

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, DRIVER_URL)

        self.assertEqual(get_user_model().objects.count(), initial_count - 1)

        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=driver_to_delete.pk)

    def test_car_delete(self):
        car_to_delete = Car.objects.get(model="Rock")

        initial_count = Car.objects.count()

        delete_url = reverse(
            "taxi:car-delete",
            kwargs={"pk": car_to_delete.pk}
        )

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, CAR_URL)

        self.assertEqual(Car.objects.count(), initial_count - 1)

        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(pk=car_to_delete.pk)

    def test_manufacturer_pagination_is_five(self):
        for i in range(5):
            Manufacturer.objects.create(
                name=f"name{i}",
                country=f"country{i}"
            )

        response = self.client.get(MANUFACTURER_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_driver_pagination_is_five(self):
        for i in range(5):
            get_user_model().objects.create(
                username=f"username{i}",
                password=f"123qwe{i}",
                license_number=f"QWE4567{i}"
            )

        response = self.client.get(DRIVER_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_car_pagination_is_five(self):
        for i in range(1, 6):
            Manufacturer.objects.create(
                name=f"manufacturer{i}",
                country=f"country{i}"
            )
            Car.objects.create(
                model=f"test{i}",
                manufacturer_id=i
            )

        response = self.client.get(CAR_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)
