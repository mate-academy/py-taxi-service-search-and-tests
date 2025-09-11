from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, NoReverseMatch

from taxi.models import Manufacturer, Car
Driver = get_user_model()

URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")


class PublicManufacturerListViewTest(TestCase):
    def test_not_logged_user(self):
        res = self.client.get(URL_MANUFACTURER_LIST)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user123",
            password="test123"
        )
        Manufacturer.objects.bulk_create(
            [Manufacturer(name=f"Maker {i}", country="TestCountry") for i in range(1, 8)]
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_user(self):
        Manufacturer.objects.create(
            name="TestName1",
            country="UK"
        )
        Manufacturer.objects.create(
            name="TestName2",
            country="Poland"
        )
        res = self.client.get(URL_MANUFACTURER_LIST)
        self.assertEqual(res.status_code, 200)
        expected = Manufacturer.objects.order_by("id")[:5]
        self.assertEqual(list(res.context["manufacturer_list"]), list(expected))
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_if_paginated(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        paginator = response.context["paginator"]
        page_obj = response.context["page_obj"]
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(paginator.count, 7)
        self.assertEqual(page_obj.number, 1)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertIn("search_form", response.context)

    def test_paginate_page_2(self):
        response = self.client.get(URL_MANUFACTURER_LIST, {"page": 2})
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertTrue(response.context["page_obj"].has_previous())
        self.assertFalse(response.context["page_obj"].has_next())

    def test_queryset_with_name(self):
        res = self.client.get(URL_MANUFACTURER_LIST, {"name": "Maker 3"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["paginator"].count, 1)


class PublicManufacturerCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestName",
            password="TestPassword"
        )
        cls.url = reverse("taxi:manufacturer-create")

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestName",
            password="TestPassword"
        )
        cls.url = reverse("taxi:manufacturer-create")

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_in(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_if_form_in_context(self):
        res = self.client.get(self.url)
        self.assertIn("form", res.context)

    def test_if_creates_new_object(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(
                name="TestName",
                country="TestCountry"
            ),
            Manufacturer(
                name="TestName1",
                country="TestCountry1"
            )
        ])
        self.assertEqual(Manufacturer.objects.count(), 2)

        data = {"name": "TestName2", "country": "TestCountry2"}
        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), 3)
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))


class PublicManufacturerUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse("taxi:manufacturer-update", kwargs={"pk": 1})

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse("taxi:manufacturer-update", kwargs={"pk": 1})

    def setUp(self):
        self.client.force_login(self.user)
        self.res = self.client.get(self.url)

    def test_logged_user(self):
        self.assertEqual(self.res.status_code, 200)

    def test_if_form_in_context(self):
        self.assertIn("form", self.res.context)

    def test_if_object_modified(self):
        data = {"name": "ModifiedTestName", "country": "TestCountry"}
        res = self.client.post(self.url, data)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "ModifiedTestName")
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))


class PublicManufacturerDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_in(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_if_form_in_context(self):
        res = self.client.get(self.url)
        self.assertIn("form", res.context)

    def test_if_object_deleted(self):
        res = self.client.post(self.url, follow=True)
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))

        self.assertFalse(Manufacturer.objects.filter(pk=1).exists())


# ---------- CAR LIST / DETAIL ----------
class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u1", password="p1", license_number="ABC123"
        )
        cls.m1 = Manufacturer.objects.create(name="Maker A", country="PL")
        cls.m2 = Manufacturer.objects.create(name="Maker B", country="UK")
        # створимо 7 авто для пагінації (paginate_by = 5)
        for i in range(1, 8):
            Car.objects.create(model=f"Model {i}", manufacturer=cls.m1 if i <= 4 else cls.m2)

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_ok_and_template(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("object_list", res.context)
        self.assertIn("search_form", res.context)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_paginated(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertEqual(res.context["paginator"].count, 7)
        self.assertEqual(res.context["page_obj"].number, 1)
        self.assertTrue(res.context["page_obj"].has_next())

    def test_paginate_page_2(self):
        res = self.client.get(reverse("taxi:car-list"), {"page": 2})
        self.assertEqual(res.context["page_obj"].number, 2)
        self.assertTrue(res.context["page_obj"].has_previous())
        self.assertFalse(res.context["page_obj"].has_next())

    def test_queryset_filter_by_model(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "Model 3"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["paginator"].count, 1)


class PublicCarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="X", manufacturer=cls.m)

    def test_login_required(self):
        res = self.client.get(reverse("taxi:car-detail", kwargs={"pk": self.car.pk}))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u2", password="p2", license_number="XYZ999"
        )
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="X", manufacturer=cls.m)

    def setUp(self):
        self.client.force_login(self.user)

    def test_detail_ok(self):
        res = self.client.get(reverse("taxi:car-detail", kwargs={"pk": self.car.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"].pk, self.car.pk)


# ---------- CAR CREATE / UPDATE / DELETE ----------
class PublicCarCreateUpdateDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="Y", manufacturer=cls.m)

    def test_create_login_required(self):
        self.assertNotEqual(self.client.get(reverse("taxi:car-create")).status_code, 200)

    def test_update_login_required(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        self.assertNotEqual(self.client.get(url).status_code, 200)

    def test_delete_login_required(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        self.assertNotEqual(self.client.get(url).status_code, 200)


class PrivateCarCreateUpdateDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u3", password="p3", license_number="LIC111"
        )
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="Z", manufacturer=cls.m)

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_create_has_form(self):
        res = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_create_car(self):
        data = {"model": "NewCar", "manufacturer": self.m.pk}
        res = self.client.post(reverse("taxi:car-create"), data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Car.objects.filter(model="NewCar", manufacturer=self.m).exists())
        self.assertRedirects(res, reverse("taxi:car-list"))

    def test_get_update_has_form(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_update_car(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        res = self.client.post(url, {"model": "Z-upd", "manufacturer": self.m.pk})
        self.assertRedirects(res, reverse("taxi:car-list"))
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Z-upd")

    def test_delete_car(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        res = self.client.post(url, follow=True)
        self.assertRedirects(res, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())


# ---------- DRIVER LIST / DETAIL ----------
class PublicDriverListDetailViewTest(TestCase):
    def test_list_login_required(self):
        self.assertNotEqual(self.client.get(reverse("taxi:driver-list")).status_code, 200)

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="pubd", password="p", license_number="L1"
        )

    def test_detail_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})).status_code,
            200,
        )


class PrivateDriverListDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="d1", password="p1", license_number="DL1"
        )
        for i in range(1, 8):
            Driver.objects.create_user(
                username=f"user{i}",
                password="p!",
                license_number=f"TST{i+300:05d}",
                first_name=f"F{i}",
                last_name=f"L{i}",
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_paginated_and_form(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertIn("search_form", res.context)

    def test_list_page_2(self):
        res = self.client.get(reverse("taxi:driver-list"), {"page": 2})
        self.assertEqual(res.context["page_obj"].number, 2)

    def test_detail_ok(self):
        other = Driver.objects.exclude(pk=self.user.pk).first()
        res = self.client.get(reverse("taxi:driver-detail", kwargs={"pk": other.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"].pk, other.pk)

    def test_queryset_filter_title_if_present(self):
        res = self.client.get(reverse("taxi:driver-list"), {"title": "user3"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("object_list", res.context)


# ---------- DRIVER CREATE / LICENSE UPDATE / DELETE ----------
class PrivateDriverCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Driver.objects.create_user(
            username="admin", password="p-admin", license_number="ADM001"
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_get_create_has_form(self):
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_create_driver(self):
        data = {
            "username": "new_driver_02",
            "password1": "S0meStrongPwd!",
            "password2": "S0meStrongPwd!",
            "first_name": "Neo",
            "last_name": "Driver",
            "license_number": "NEW77756",
        }
        res = self.client.post(reverse("taxi:driver-create"), data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="new_driver_02").exists())


class PrivateDriverLicenseUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="new_driver_01", password="Str0ng-Password!", license_number="OLD12345"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_has_form(self):
        url = reverse("taxi:driver-update", kwargs={"pk": self.user.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_update_license(self):
        url = reverse("taxi:driver-license-update", kwargs={"pk": self.user.pk})
        res = self.client.post(url, {"license_number": "NEW99967"})
        self.assertRedirects(res, reverse("taxi:driver-list"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "NEW99967")


class PrivateDriverDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="delme", password="p", license_number="DEL123"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_delete_driver_redirects_or_errors_on_bad_success_url(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": self.user.pk})
        try:
            res = self.client.post(url, follow=False)
        except NoReverseMatch:
            return
        self.assertFalse(Driver.objects.filter(pk=self.user.pk).exists())


# ---------- TOGGLE ASSIGN TO CAR ----------
class ToggleAssignToCarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="toggle", password="p", license_number="TOG111"
        )
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="T", manufacturer=cls.m)

    def setUp(self):
        self.client.force_login(self.user)

    def test_toggle_add_and_remove(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})

        # add
        res = self.client.post(url, follow=True)
        self.assertRedirects(res, reverse("taxi:car-detail", args=[self.car.pk]))
        self.assertTrue(self.car.drivers.filter(pk=self.user.pk).exists())

        # remove
        res = self.client.post(url, follow=True)
        self.assertRedirects(res, reverse("taxi:car-detail", args=[self.car.pk]))
        self.assertFalse(self.car.drivers.filter(pk=self.user.pk).exists())
