from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import LICENSE_ERRORS
from taxi.models import Manufacturer, Car, Driver

HOME_PAGE = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicHomePageTest(TestCase):
    def test_login_required(self):
        res = self.client.get(HOME_PAGE)
        self.assertNotEqual(res.status_code, 200)


class PrivateHomePageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            license_number="AAA123456",
            password="TestPassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country",
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )
        response = self.client.get(HOME_PAGE)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_manufacturers"], 2)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 0)
        self.assertTemplateUsed(response, "taxi/index.html")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            license_number="AAA123456",
            password="TestPassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country",
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = list(Manufacturer.objects.all())
        response_manufacturers = list(response.context["manufacturer_list"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(manufacturers, response_manufacturers)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_form(self):
        test_keys = {1: "", 2: "Audi", 3: "BMW", 4: "w"}
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        manufacturers = Manufacturer.objects.all()

        response = self.client.get(
            MANUFACTURER_URL, {"manufacturer": test_keys[1]}
        )
        self.assertIn("search_form", response.context)
        search_value_key = response.context_data[
            "search_form"]["manufacturer"].value()
        db_q = manufacturers.filter(name__icontains=test_keys[1])
        self.assertEqual(search_value_key, test_keys[1])
        self.assertQuerysetEqual(db_q, response.context_data["object_list"])

        for key, value in test_keys.items():
            if key != 1:
                response = self.client.get(
                    MANUFACTURER_URL,
                    {"manufacturer": value}
                )
                search_value_key = response.context_data["search_form"][
                    "manufacturer"
                ].value()
                db_q = manufacturers.filter(name__icontains=value)
                self.assertNotEqual(search_value_key, test_keys[key - 1])
                self.assertEqual(search_value_key, value)
                self.assertQuerysetEqual(
                    db_q,
                    response.context_data["object_list"]
                )

    def test_is_page_contain_paginator(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertIn("paginator", res.context)

    def test_is_pagination_appears(self):
        test_keys = {1: False, 2: False, 3: True}
        res = self.client.get(MANUFACTURER_URL)
        pagination_per_page = res.context_data["paginator"].per_page
        self.assertFalse(res.context_data["is_paginated"], test_keys[1])
        for i in range(pagination_per_page):
            Manufacturer.objects.create(
                name=f"Test manufacturer {i}", country=f"Test country {i}"
            )
        res = self.client.get(MANUFACTURER_URL)
        self.assertFalse(res.context_data["is_paginated"], test_keys[2])
        Manufacturer.objects.create(
            name=f"Test manufacturer {i + 1}", country=f"Test country {i + 1}"
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertTrue(res.context_data["is_paginated"], test_keys[3])

    def test_is_pagination_disappears(self):
        test_keys = {1: True, 2: False}
        res = self.client.get(MANUFACTURER_URL)
        pagination_per_page = res.context_data["paginator"].per_page

        for i in range(pagination_per_page + 1):
            Manufacturer.objects.create(
                name=f"Test manufacturer {i}", country=f"Test country {i}"
            )

        res = self.client.get(MANUFACTURER_URL)
        self.assertTrue(res.context_data["is_paginated"], test_keys[1])
        Manufacturer.objects.get(id=1).delete()
        res = self.client.get(MANUFACTURER_URL)
        self.assertFalse(res.context_data["is_paginated"], test_keys[2])

    def test_next_page_pagination_with_save_qwery_param(self):
        test_keys = {
            1: {},
            2: {"manufacturer": "", "page": 1},
            3: {"manufacturer": "", "page": 2},
            4: {"manufacturer": "a", "page": 1},
            5: {"manufacturer": "a", "page": 2},
            6: {"manufacturer": "T", "page": 1},
        }
        manufacturers = {
            "Toyota": "Japan",
            "BMW": "Germany",
            "Ford": "USA",
            "Hyundai": "South Korea",
            "Ferrari": "Italy",
            "Renault": "France",
            "Volvo": "Sweden",
            "Volkswagen": "Germany",
            "Kia": "South Korea",
            "Chevrolet": "USA",
            "ZAZ": "Ukraine",
        }
        res = self.client.get(MANUFACTURER_URL, test_keys[1])
        pagination_per_page = res.context_data["paginator"].per_page

        for manufacturer, country in manufacturers.items():
            Manufacturer.objects.create(name=manufacturer, country=country)

        for i in range(2, 5, 2):
            db_q = Manufacturer.objects.filter(
                name__icontains=test_keys[i]["manufacturer"]
            )
            res = self.client.get(MANUFACTURER_URL, test_keys[i])
            self.assertQuerysetEqual(
                res.context_data["manufacturer_list"],
                db_q[:pagination_per_page]
            )
            res = self.client.get(MANUFACTURER_URL, test_keys[i + 1])
            self.assertQuerysetEqual(
                res.context_data["manufacturer_list"],
                db_q[pagination_per_page: pagination_per_page * 2],
            )

    def test_create_button(self):
        """
        Test checking:
        - The page has a Create button;
        - The Create button has right url;
        """
        res = self.client.get(MANUFACTURER_URL)
        self.assertContains(res, "Create")
        self.assertContains(
            res,
            reverse("taxi:manufacturer-create"), html=False
        )

    def test_is_manufacturer_row_has_links(self):
        """
        Test that checking if a manufacturer has:
        - create link;
        - delete link.
        """
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country"
        )
        res = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.get(
            name="Test Manufacturer"
        )
        self.assertContains(
            res,
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}
            )
        )
        self.assertContains(
            res,
            reverse(
                "taxi:manufacturer-delete", kwargs={"pk": manufacturer.id}
            )
        )

    def test_update_manufacturer(self):
        """
        Test checks:
        - Is fields filled (html page contains, form initial contains);
        - Is right template used;
        - Is right page label;
        - Is manufacturer has new name and country;
        - Is redirect after update manufacturer;
        - Is right redirect page after redirect.
        """
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        manufacturer = Manufacturer.objects.get(id=1)
        res = self.client.get(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": manufacturer.id}
            )
        )
        self.assertContains(res, manufacturer.name)
        self.assertContains(res, manufacturer.country)
        self.assertEqual(
            res.context_data["form"].initial,
            {
                "id": manufacturer.id,
                "name": manufacturer.name,
                "country": manufacturer.country
            }
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_form.html")
        self.assertContains(res, "Update manufacturer")
        res.context["form"].initial["name"] = "Audi"
        res.context["form"].initial["country"] = "Deutschland"
        res = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": manufacturer.id}
            ),
            res.context["form"].initial
        )
        self.assertEqual(manufacturer, Manufacturer.objects.get(id=1))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("taxi:manufacturer-list"))

    def test_delete_manufacturer(self):
        """
        Test checks:
         - is on the right url;
         - is right template used;
         - is right redirect page;
         - is new manufacturer in db;
         - is deleted manufacturer from db.
         - is status code is 302;
         - is right ulr in response after post method.

        """
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        manufacturer = Manufacturer.objects.get(id=1)
        res = self.client.get(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer.id}
            )
        )
        self.assertEqual(
            res.context["request"].path_info,
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer.id}
            )
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_confirm_delete.html"
        )
        self.assertTrue(manufacturer in Manufacturer.objects.all())
        res = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer.id}
            )
        )
        self.assertFalse(manufacturer in Manufacturer.objects.all())
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("taxi:manufacturer-list"))


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            license_number="AAA123456",
            password="TestPassword123"
        )
        self.client.force_login(self.user)

    def test_cars(self):
        """
        The test checking:
        - Is status_code equal 200;
        - Is retrieve cars;
        - Is right page template;
        - Is the page has search form;
        - Is search value has default value '';
        - Is right query on the first page with default value;
        - Is right queries with different value;
        - Is the page has a paginator;
        - Is pagination disappears;
        - Test page has a Create button;
        - The Create button has right url;
        - Is car row has link of the car;
        """
        test_keys = {1: "", 2: "Corolla", 3: "XC90", 4: "o"}
        test_keys_paginator = {1: True, 2: False}
        manufacturers = {
            "Toyota": "Japan",
            "BMW": "Germany",
            "Ford": "USA",
            "Hyundai": "South Korea",
            "Ferrari": "Italy",
            "Renault": "France",
            "Volvo": "Sweden",
            "Volkswagen": "Germany",
            "Kia": "South Korea",
            "Chevrolet": "USA",
        }
        models = {
            "Toyota": "Corolla",
            "BMW": "320i",
            "Ford": "Mustang",
            "Hyundai": "Elantra",
            "Ferrari": "488 GTB",
            "Renault": "Clio",
            "Volvo": "XC90",
            "Volkswagen": "Golf",
            "Kia": "Sportage",
            "Chevrolet": "Camaro"
        }

        current_driver = Driver.objects.get(id=1)
        cars = Car.objects.all()

        for manufacturer, country in manufacturers.items():
            Manufacturer.objects.create(name=manufacturer, country=country)
            manufacturer_db = Manufacturer.objects.get(name=manufacturer)
            new_car = Car.objects.create(
                model=models[manufacturer],
                manufacturer=manufacturer_db
            )
            new_car.drivers.add(current_driver)
            new_car.save()
        response = self.client.get(CAR_LIST_URL)
        paginator_per_page = response.context["paginator"].per_page
        search_value_key = response.context["search_form"]["model"].value()
        db_q = cars.filter(model__icontains=test_keys[1])[:paginator_per_page]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(Car.objects.all()[:paginator_per_page]),
            list(response.context["car_list"])
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn("search_form", response.context)
        self.assertEqual(search_value_key, test_keys[1])
        self.assertEqual(
            list(db_q),
            list(response.context_data["object_list"])
        )

        for key, value in test_keys.items():
            if key != 1:
                response = self.client.get(CAR_LIST_URL, {"model": value})
                search_value_key = response.context_data["search_form"][
                    "model"
                ].value()
                db_q = cars.filter(model__icontains=value)
                self.assertNotEqual(search_value_key, test_keys[key - 1])
                self.assertEqual(search_value_key, value)
                self.assertEqual(
                    list(db_q), list(response.context_data["object_list"])
                )

        response = self.client.get(CAR_LIST_URL)
        self.assertIn("paginator", response.context, )
        self.assertTrue(
            response.context_data["is_paginated"],
            test_keys_paginator[1]
        )
        response = self.client.get(CAR_LIST_URL, {"model": "Camaro"})
        self.assertFalse(
            response.context_data["is_paginated"],
            test_keys_paginator[2]
        )
        self.assertContains(response, "Create")
        self.assertContains(
            response,
            reverse("taxi:car-create"), html=False
        )
        self.assertContains(
            response,
            reverse(
                "taxi:car-detail",
                kwargs={"pk": response.context["object_list"][0].id}
            )
        )

    def test_detail_car(self):
        """
        The test checking:
        - Is status_code equal 200;
        - If the page has Update button;
        - The Update button has right url;
        - If the page has Delete button;
        - The Delete button has right url;
        - Check the logged user is absence in list of drivers;
        - If the page has 'Assign me to this car' button;
        - Is right page status with redirect request;
        - Check the logged user in list of drivers;
        - Text in button change from 'Assign me to this car'
          to 'Delete me from this car';
        - Car update form has a right template;
        - Is page label has 'Update car';
        - Check the initial data after assign driver;
        - Check page status after update data about car;
        - Is right redirect page after update data about car;
        - Is right car model name on car list page;
        - Is right drivers use the car;
        - Is initial drivers changed after post method with all drivers;
        - Is car delete page has a right template;
        - Is post method has a redirect status_code;
        - Is post method has right redirect url;
        - Is car deleted after post method;
        """
        manufacturers = {
            "name": "Toyota",
            "country": "Japan",
        }
        models = {
            1: "Corolla",
            2: "Supra",
        }
        initial_update_keys = {
            1: {
                "drivers": [Driver.objects.get(username="test.user")],
                "model": models[1],
                "manufacturer": 1,
                "id": 1,
            },
            2: {
                "drivers": [Driver.objects.get(username="test.user")],
                "model": "Supra",
                "manufacturer": 1,
                "id": 1,
            },
        }
        db_manufacturer = Manufacturer.objects.create(
            name=manufacturers["name"],
            country=manufacturers["country"]
        )
        db_car = Car.objects.create(
            model=models[1],
            manufacturer=db_manufacturer
        )
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update")
        self.assertContains(
            response,
            reverse("taxi:car-update", kwargs={"pk": db_car.id})
        )
        self.assertContains(response, "Delete")
        self.assertContains(
            response,
            reverse("taxi:car-delete", kwargs={"pk": db_car.id})
        )
        self.assertNotContains(response, response.context["user"].__str__())
        self.assertContains(response, "Assign me to this car")
        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign", kwargs={"pk": db_car.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertContains(response, response.context["user"].__str__())
        self.assertContains(response, "Delete me from this car")
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": db_car.id})
        )
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertContains(response, "Update car")
        self.assertEqual(
            response.context_data["form"].initial,
            initial_update_keys[1]
        )

        response = self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": db_car.id}
            ),
            {
                "model": models[2],
                "manufacturer": db_car.id,
                "drivers": db_car.drivers.values_list(
                    "id",
                    flat=True
                ),
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("taxi:car-list"))
        response = self.client.get(response.url)
        self.assertContains(response, models[2])
        get_user_model().objects.create_user(
            username="test.user2",
            license_number="AAA000000",
            password="TestPassword123"
        )
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": db_car.id})
        )
        ds_in_initial_form = response.context["form"].initial["drivers"]
        ds_in_checkbox_list = list(
            response.context["form"].fields["drivers"].queryset
        )
        self.assertNotEqual(ds_in_initial_form, ds_in_checkbox_list)
        drivers_ids = list(Driver.objects.all().values_list("id", flat=True))
        self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": db_car.id}
            ),
            {
                "model": models[2],
                "manufacturer": db_car.id,
                "drivers": drivers_ids,
            }
        )
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": db_car.id})
        )
        self.assertEqual(
            response.context["form"].initial["drivers"],
            ds_in_checkbox_list
        )
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": db_car.id})
        )
        self.assertTemplateUsed(
            response, "taxi/car_confirm_delete.html"
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": db_car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.all().count(), 0)

    def test_car_create(self):
        """
        Test checks:
        - Is the page has right template;
        - Is post request has status_code 302;
        - Is response has right redirect url;
        - Is the car created successfully;
        """
        models = {
            1: "Celika",
        }
        manufacturers = {
            "name": "Toyota",
            "country": "Japan",
        }
        db_manufacturer = Manufacturer.objects.create(
            name=manufacturers["name"],
            country=manufacturers["country"]
        )
        response = self.client.get(reverse("taxi:car-create"))
        self.assertTemplateUsed(response, "taxi/car_form.html")
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": models[1],
                "drivers": self.user.id,
                "manufacturer": db_manufacturer.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("taxi:car-list"))
        self.assertTrue(Car.objects.filter(model__icontains=models[1]))


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            license_number="AAA000000",
            password="TestPassword123"
        )
        self.client.force_login(self.user)

    def test_drivers(self):
        """
        The test checking:
        - Is status_code equal 200;
        - Is right page template;
        - Is the page has search form;
        - Is search value has default value '';
        - Is right query on the first page with default value;
        - Is right queries with different value;
        - Test page has a Create button;
        - The Create button has right url;
        - Is driver row has link of the driver;
        """
        test_keys = {1: "", 2: "user", 3: "user.00", 4: "1"}
        drivers = [
            {
                "username": "user.001",
                "first_name": "Maksym",
                "last_name": "Protsak",
                "license_number": "AAA123456"
            },
            {
                "username": "user.002",
                "first_name": "Ivan",
                "last_name": "Petrenko",
                "license_number": "BBB654321"
            },
            {
                "username": "user.003",
                "first_name": "Oleh",
                "last_name": "Ivanenko",
                "license_number": "CCC987654"
            },
            {
                "username": "user.004",
                "first_name": "Serhii",
                "last_name": "Kovalenko",
                "license_number": "DDD321654"
            },
            {
                "username": "user.005",
                "first_name": "Andrii",
                "last_name": "Shevchenko",
                "license_number": "EEE123789"
            },
            {
                "username": "user.006",
                "first_name": "Oleksandr",
                "last_name": "Bondarenko",
                "license_number": "FFF456789"
            },
            {
                "username": "user.007",
                "first_name": "Dmytro",
                "last_name": "Shapoval",
                "license_number": "GGG654987"
            },
            {
                "username": "user.008",
                "first_name": "Volodymyr",
                "last_name": "Tkachenko",
                "license_number": "HHH789456"
            },
            {
                "username": "user.009",
                "first_name": "Yurii",
                "last_name": "Kryvyi",
                "license_number": "III987321"
            },
            {
                "username": "user.010",
                "first_name": "Roman",
                "last_name": "Horbach",
                "license_number": "JJJ321789"
            }
        ]

        for driver in drivers:
            Driver.objects.create(
                username=driver["username"],
                first_name=driver["first_name"],
                last_name=driver["last_name"],
                license_number=driver["license_number"]
            )
        drivers = Driver.objects.all()
        response = self.client.get(DRIVER_LIST_URL)
        paginator_per_page = response.context["paginator"].per_page
        search_value_key = response.context["search_form"]["driver"].value()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )
        self.assertIn("search_form", response.context)
        self.assertEqual(search_value_key, test_keys[1])
        self.assertEqual(
            list(Driver.objects.all()[:paginator_per_page]),
            list(response.context["driver_list"])
        )
        for key, value in test_keys.items():
            if key != 1:
                response = self.client.get(DRIVER_LIST_URL, {"driver": value})
                search_value_key = response.context_data["search_form"][
                    "driver"
                ].value()
                db_q = drivers.filter(
                    username__icontains=value
                )[:paginator_per_page]
                self.assertNotEqual(search_value_key, test_keys[key - 1])
                self.assertEqual(search_value_key, value)
                self.assertEqual(
                    list(db_q), list(response.context_data["object_list"])
                )
        self.assertContains(response, "Create")
        self.assertContains(
            response,
            reverse("taxi:driver-create"), html=False
        )
        self.assertContains(
            response,
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": response.context["object_list"][0].id}
            )
        )

    def test_detail_driver(self):
        """
        The test checking:
        - Is status_code equal to 200;
        - If the page has 'Update license number' button;
        - The 'Update license number' button has right url;
        - If the page has Delete button;
        - The Delete button has right url;
        - Driver detail form has a right template;
        - Driver update license form has a right template;
        - Is right page label;
        - Check initial data of update license form;
        - Take form errors or license number;
        - Is right status_code after post request;
        - Is right redirect url;
        - Is driver license updated in db;
        - Is drivers list page has a new license number;
        - Delete driver from db.
        - Is right status_code after post request;
        - Is right redirect url;
        >- Is drivers list empty;
        """
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        initial_test_keys = {
            1: self.user.license_number,
            2: "123456789",
            3: "12345678",
            4: "ABCD1234",
            5: "ABC12345"
        }
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update license number")
        self.assertContains(
            response,
            reverse("taxi:driver-update", kwargs={"pk": self.user.id})
        )
        self.assertContains(response, "Delete")
        self.assertContains(
            response,
            reverse("taxi:driver-delete", kwargs={"pk": self.user.id})
        )
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertContains(response, "Update driver license")
        self.assertEqual(
            response.context["form"].initial["license_number"],
            initial_test_keys[1]
        )

        for i in range(2, len(initial_test_keys) - 1):
            response = self.client.post(
                reverse("taxi:driver-update", kwargs={"pk": 1}),
                {"license_number": initial_test_keys[i]}
            )
            self.assertEqual(
                response.context["form"].errors["license_number"][0],
                LICENSE_ERRORS[i - 1]
            )
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": 1}),
            {"license_number": initial_test_keys[5]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("taxi:driver-list"))
        self.assertEqual(
            Driver.objects.get(id=self.user.id).license_number,
            initial_test_keys[5]
        )
        response = self.client.get(response.url)
        self.assertContains(response, initial_test_keys[5])
        response = self.client.post(
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": 1}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("taxi:driver-list"))
        self.assertEqual(Driver.objects.all().count(), 0)
