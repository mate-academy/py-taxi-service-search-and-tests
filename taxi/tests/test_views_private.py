from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>")
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Manufacturer", country="USA")
        Manufacturer.objects.create(name="Manufacturer2", country="Ukraine")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        list_manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(list_manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        man = Manufacturer.objects.create(name="Manufacturer", country="USA")
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertContains(res, man.name)
        self.assertContains(res, man.country)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_update_manufacturer(self):
        man = Manufacturer.objects.create(name="Manufacturer", country="USA")
        manufacturer_update_url = reverse("taxi:manufacturer-update",
                                          kwargs={"pk": man.id})
        response = self.client.get(manufacturer_update_url)
        self.assertEqual(response.status_code, 200)
        new_man = Manufacturer.objects.get(id=man.id)
        new_man.name = "Manufacturer2"
        new_man.country = "Ukraine"
        new_man.save()
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertContains(res, new_man.name)
        self.assertContains(res, new_man.country)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_delete_manufacturer(self):
        man = Manufacturer.objects.create(name="Manufacturer", country="USA")
        manufacturer_delete_url = reverse("taxi:manufacturer-delete",
                                          kwargs={"pk": man.id})
        response = self.client.get(manufacturer_delete_url)
        self.assertEqual(response.status_code, 200)
        Manufacturer.objects.get(id=man.id).delete()
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotContains(res, man)
        self.assertTemplateUsed("taxi/manufacturer_confirm_delete.html")

    def test_retrieve_car_list(self):
        vol = Manufacturer.objects.create(name="Volkswagen", country="Germany")
        Car.objects.create(model="Golf", manufacturer=vol)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        list_cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(list_cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_create(self):
        man = Manufacturer.objects.create(name="Volkswagen", country="Germany")
        car = Car.objects.create(model="Golf", manufacturer=man)
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        res = self.client.get(CAR_LIST_URL)
        self.assertContains(res, car.model)
        self.assertContains(res, man.name)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_update_car(self):
        man = Manufacturer.objects.create(name="Volkswagen", country="Germany")
        man_second = Manufacturer.objects.create(name="Alpha Romeo",
                                                 country="Italy")
        car = Car.objects.create(model="Golf", manufacturer=man)
        car_update_url = reverse("taxi:car-update", kwargs={"pk": car.id})
        response = self.client.get(car_update_url)
        self.assertEqual(response.status_code, 200)
        new_car = Car.objects.get(id=car.id)
        new_car.model = "Julia"
        new_car.manufacturer = man_second
        new_car.save()
        res = self.client.get(CAR_LIST_URL)
        self.assertContains(res, new_car.model)
        self.assertContains(res, man_second.name)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_delete(self):
        man = Manufacturer.objects.create(name="Volkswagen", country="Germany")
        car = Car.objects.create(model="Golf", manufacturer=man)
        car_delete_url = reverse("taxi:car-delete", kwargs={"pk": car.id})
        response = self.client.get(car_delete_url)
        self.assertEqual(response.status_code, 200)
        car.delete()
        res = self.client.get(CAR_LIST_URL)
        self.assertNotContains(res, car)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_detail(self):
        man = Manufacturer.objects.create(name="Volkswagen", country="Germany")
        car = Car.objects.create(model="Golf", manufacturer=man)
        car_detail_url = reverse("taxi:car-detail", kwargs={"pk": car.id})
        response = self.client.get(car_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, car.model)
        self.assertContains(response, man.name)
        self.assertContains(response, man.country)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_retrieve_driver_list(self):
        Driver.objects.create(
            username="Lamuk",
            first_name="Dima",
            last_name="Dobkin",
            license_number="ARC12345"
        )
        Driver.objects.create(username="Sergun",
                              first_name="Sergiy",
                              last_name="Yurov",
                              license_number="LDG54378"
                              )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        list_drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]),
                         list(list_drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_create(self):
        form_data = {
            "username": "valuc",
            "password1": "Test22021994",
            "password2": "Test22021994",
            "first_name": "Dmitriy",
            "last_name": "Dobkin",
            "license_number": "KLB12345",
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_delete(self):
        driver = Driver.objects.create(
            username="Kolin",
            first_name="Dima",
            last_name="Durbin",
            license_number="ARB12345"
        )
        driver_delete_url = reverse("taxi:driver-delete",
                                    kwargs={"pk": driver.id})
        response = self.client.get(driver_delete_url)
        self.assertEqual(response.status_code, 200)
        Driver.objects.filter(pk=driver.id).delete()
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotContains(res, driver)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_driver_detail(self):
        driver = Driver.objects.create(
            username="Kolin",
            first_name="Dima",
            last_name="Durbin",
            license_number="ARB12345"
        )
        driver_detail_url = reverse("taxi:driver-detail",
                                    kwargs={"pk": driver.id})
        response = self.client.get(driver_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, driver.username)
        self.assertContains(response, driver.first_name)
        self.assertContains(response, driver.last_name)
        self.assertContains(response, driver.license_number)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_license_number_update(self):
        driver = Driver.objects.create(
            username="Kolin",
            first_name="Dima",
            last_name="Durbin",
            license_number="ARB12345"
        )
        driver.license_number = "KLB12345"
        driver.save()
        self.assertTrue(driver.license_number, "KLB12345")
