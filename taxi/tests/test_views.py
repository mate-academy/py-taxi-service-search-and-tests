from django.contrib.auth import get_user_model
from django.db.models import Max
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView, CarListView, DriverListView


def create_manufacturers(count: int, name_prefix: str = "test") -> None:
    for index in range(count):
        Manufacturer.objects.create(
            name=f"{name_prefix}_name_{index + 1}",
            country=f"{name_prefix}_country_{index + 1}"
        )


def create_cars(count: int, name_prefix: str = "test") -> None:
    manufacturer = Manufacturer.objects.get_or_create(
        name="test_name",
        country="test_country"
    )

    for index in range(count):
        Car.objects.create(
            model=f"{name_prefix}_model_{index + 1}",
            manufacturer=manufacturer[0]
        )


def create_drivers(count: int, name_prefix: str = "test") -> None:
    max_pk = get_user_model().objects.aggregate(Max("pk"))
    start_index = max_pk.get("pk__max", 0) + 1

    for index in range(start_index, start_index + count):
        get_user_model().objects.create(
            username=f"{name_prefix}_username_{index + 1}",
            password="1234567",
            license_number="ABC" + f"{index}".zfill(5)
        )


class IndexViewTest(TestCase):
    url = reverse("taxi:index")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

    def test_index_view_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)

    def test_context_data_num_cars(self) -> None:
        num_exist_cars = Car.objects.count()
        new_cars = 5
        create_cars(new_cars)
        num_cars = num_exist_cars + new_cars

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_cars"], num_cars)

    def test_context_data_num_manufacturers(self) -> None:
        num_exist_manufacturers = Manufacturer.objects.count()
        new_manufacturers = 5
        create_manufacturers(new_manufacturers)
        num_manufacturers = num_exist_manufacturers + new_manufacturers

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_manufacturers"],
                         num_manufacturers)

    def test_context_data_num_drivers(self) -> None:
        num_exist_drivers = get_user_model().objects.count()
        new_drivers = 5
        create_drivers(new_drivers)
        num_drivers = num_exist_drivers + new_drivers

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], num_drivers)

    def test_context_data_num_visits(self) -> None:
        num_visits = 10

        for _ in range(num_visits):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_visits"], num_visits)

    def test_index_page_used_correct_template(self) -> None:
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/index.html")


class ManufacturerListViewTest(TestCase):
    url = reverse("taxi:manufacturer-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

        create_manufacturers(count=5)

    def test_manufacturer_list_view_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_receive_manufacturer_list(self) -> None:
        expected_qs = Manufacturer.objects.all()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            expected_qs
        )

    def test_manufacturer_list_paginated(self) -> None:
        paginate_by = ManufacturerListView.paginate_by

        if paginate_by >= Manufacturer.objects.count():
            additional_count = paginate_by - Manufacturer.objects.count() + 1
            create_manufacturers(additional_count, name_prefix="paginated")

        expected_qs = Manufacturer.objects.all()[:paginate_by]
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            expected_qs
        )

        response = self.client.get(self.url, data={"page": 2})
        expected_qs = Manufacturer.objects.all()[paginate_by: paginate_by * 2]
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            expected_qs
        )

    def test_manufacturer_search(self) -> None:
        search_value = "name_5"
        expected_qs = Manufacturer.objects.all().filter(
            name__icontains=search_value
        )

        response = self.client.get(self.url,
                                   data={"search_input": search_value})

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            expected_qs
        )

    def test_manufacturer_template(self) -> None:
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerCreateViewTest(TestCase):
    url = reverse("taxi:manufacturer-create")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

    def test_manufacturer_create_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_view_redirect_to_correct_url(self) -> None:
        post_data = {
            "name": "Test name",
            "country": "Test country"
        }

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url, data=post_data)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class ManufacturerUpdateViewTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        self.url = reverse("taxi:manufacturer-update",
                           kwargs={"pk": self.manufacturer.pk})

    def test_manufacturer_update_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_view_redirect_to_correct_url(self) -> None:
        post_data = {
            "name": "New name",
            "country": "New country"
        }

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url, data=post_data)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class ManufacturerDeleteViewTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        self.url = reverse("taxi:manufacturer-delete",
                           kwargs={"pk": self.manufacturer.pk})

    def test_manufacturer_delete_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_view_redirect_to_correct_url(self) -> None:
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class CarListViewTest(TestCase):
    url = reverse("taxi:car-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

        create_cars(count=5)

    def test_car_list_view_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_receive_car_list(self) -> None:
        expected_qs = Car.objects.all()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context["car_list"],
            expected_qs,
            ordered=False
        )

    def test_car_list_paginated(self) -> None:
        paginate_by = CarListView.paginate_by

        if paginate_by >= Car.objects.count():
            additional_count = paginate_by - Car.objects.count() + 1
            create_cars(additional_count, name_prefix="paginated")

        expected_qs = Car.objects.all()[:paginate_by]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            expected_qs,
            ordered=False
        )

        expected_qs = Car.objects.all()[paginate_by: paginate_by * 2]
        response = self.client.get(self.url, data={"page": 2})
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context["car_list"],
            expected_qs,
            ordered=False
        )

    def test_car_search(self) -> None:
        search_value = "model_5"
        expected_qs = Car.objects.all().filter(model__icontains=search_value)

        response = self.client.get(self.url,
                                   data={"search_input": search_value})

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            expected_qs
        )

    def test_car_template(self) -> None:
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarDetailViewTest(TestCase):

    def test_car_detail_login_required(self) -> None:
        user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )

        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

        url = reverse("taxi:car-detail", kwargs={"pk": car.pk})

        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class CarCreateViewTest(TestCase):
    url = reverse("taxi:car-create")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

    def test_car_create_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_view_redirect_to_correct_url(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        post_data = {
            "model": "Test model",
            "manufacturer": manufacturer.pk,
            "drivers": [self.user.pk, ]
        }
        response = self.client.post(self.url, data=post_data)

        self.assertRedirects(response, reverse("taxi:car-list"))


class CarUpdateViewTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

        self.url = reverse("taxi:car-update", kwargs={"pk": car.pk})

    def test_car_update_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_view_redirect_to_correct_url(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test new name",
            country="Test country"
        )

        post_data = {
            "model": "New model",
            "manufacturer": manufacturer.pk,
            "drivers": [self.user.pk, ]
        }
        response = self.client.post(self.url, data=post_data)

        self.assertRedirects(response, reverse("taxi:car-list"))


class CarDeleteViewTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

        self.url = reverse("taxi:car-delete", kwargs={"pk": car.pk})

    def test_car_delete_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_view_redirect_to_correct_url(self) -> None:
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse("taxi:car-list"))


class DriverListViewTest(TestCase):
    url = reverse("taxi:driver-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

    def test_driver_list_view_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_receive_driver_list(self) -> None:
        create_drivers(3)
        expected_qs = get_user_model().objects.all()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            expected_qs,
            ordered=False
        )

    def test_driver_list_paginated(self) -> None:
        paginate_by = DriverListView.paginate_by

        if paginate_by >= get_user_model().objects.count():
            count = paginate_by - get_user_model().objects.count() + 1
            create_drivers(count, name_prefix="paginated")

        expected_qs = get_user_model().objects.all()[:paginate_by]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            expected_qs,
            ordered=False
        )

        expected_qs = get_user_model().objects.all()[paginate_by:
                                                     paginate_by * 2]
        response = self.client.get(self.url, data={"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            expected_qs,
            ordered=False
        )

    def test_driver_search(self) -> None:
        search_value = "username_5"
        expected_qs = get_user_model().objects.all().filter(
            username__icontains=search_value
        )

        response = self.client.get(self.url,
                                   data={"search_input": search_value})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            expected_qs
        )

    def test_driver_template(self) -> None:
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverDetailViewTest(TestCase):

    def test_driver_detail_login_required(self) -> None:
        user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )

        url = reverse("taxi:driver-detail", kwargs={"pk": user.pk})

        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class DriverCreateViewTest(TestCase):
    url = reverse("taxi:driver-create")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

    def test_driver_create_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_view_redirect_to_correct_url(self) -> None:
        post_data = {
            "username": "test.admin.username",
            "password1": "ahHsnn231Nm",
            "password2": "ahHsnn231Nm",
            "license_number": "ABC12345"
        }
        response = self.client.post(self.url, data=post_data)

        driver = get_user_model().objects.get(username="test.admin.username")
        self.assertRedirects(response,
                             reverse("taxi:driver-detail",
                                     kwargs={"pk": driver.pk}))


class DriverUpdateViewTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

        self.url = reverse("taxi:driver-update", kwargs={"pk": self.user.pk})

    def test_driver_update_login_required(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_view_redirect_to_correct_url(self) -> None:
        post_data = {
            "username": "test.admin.username",
            "first_name": "test first name",
            "last_name": "test last name",
            "license_number": "CBA12345"
        }
        response = self.client.post(self.url, data=post_data)
        self.assertRedirects(response, reverse("taxi:driver-list"))


class ToggleAssignToCarView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="12345qwe"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        self.car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

        self.url = reverse("taxi:toggle-car-assign",
                           kwargs={"pk": self.car.pk})

    def test_login_required(self) -> None:
        self.client.logout()

        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_assign_car_to_user(self) -> None:
        self.assertFalse(self.user in self.car.drivers.all())
        self.client.get(self.url)
        self.assertTrue(self.user in self.car.drivers.all())

    def test_removed_car_from_user(self) -> None:
        self.car.drivers.add(self.user)
        self.client.get(self.url)
        self.assertFalse(self.user in self.car.drivers.all())
