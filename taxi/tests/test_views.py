# taxi/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

Driver = get_user_model()


class PublicManufacturerListViewTest(TestCase):
    def test_not_logged_user(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="user123",
            password="test123",
            license_number="ABC00011",
        )
        Manufacturer.objects.bulk_create(
            [Manufacturer(name=f"Maker {i}", country="TestCountry")
             for i in range(1, 8)]
        )
        cls.url_list = reverse("taxi:manufacturer-list")
        cls.url_create = reverse("taxi:manufacturer-create")

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_user(self):
        Manufacturer.objects.create(name="TestName1", country="UK")
        Manufacturer.objects.create(name="TestName2", country="Poland")
        res = self.client.get(self.url_list)
        self.assertEqual(res.status_code, 200)
        expected = Manufacturer.objects.order_by("id")[:5]
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(expected)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_if_paginated(self):
        response = self.client.get(self.url_list)
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
        response = self.client.get(self.url_list, {"page": 2})
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertTrue(response.context["page_obj"].has_previous())
        self.assertFalse(response.context["page_obj"].has_next())

    def test_queryset_with_name(self):
        res = self.client.get(self.url_list, {"name": "Maker 3"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["paginator"].count, 1)


class PublicManufacturerCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="TestName",
            password="TestPassword",
            license_number="CR800011",
        )
        cls.url = reverse("taxi:manufacturer-create")

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="TestName",
            password="TestPassword",
            license_number="CR800012",
        )
        cls.url_create = reverse("taxi:manufacturer-create")
        cls.url_list = reverse("taxi:manufacturer-list")

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_in(self):
        res = self.client.get(self.url_create)
        self.assertEqual(res.status_code, 200)

    def test_if_form_in_context(self):
        res = self.client.get(self.url_create)
        self.assertIn("form", res.context)

    def test_if_creates_new_object(self):
        Manufacturer.objects.bulk_create(
            [
                Manufacturer(name="TestName", country="TestCountry"),
                Manufacturer(name="TestName1", country="TestCountry1"),
            ]
        )
        self.assertEqual(Manufacturer.objects.count(), 2)

        data = {"name": "TestName2", "country": "TestCountry2"}
        res = self.client.post(self.url_create, data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), 3)
        self.assertRedirects(res, self.url_list)


class PublicManufacturerUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="UPD00011",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": cls.manufacturer.pk}
        )

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="UPD00012",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": cls.manufacturer.pk}
        )
        cls.url_list = reverse("taxi:manufacturer-list")

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
        self.assertRedirects(res, self.url_list)


class PublicManufacturerDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="DEL00011",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": cls.manufacturer.pk}
        )

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="DEL00012",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        cls.url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": cls.manufacturer.pk}
        )
        cls.url_list = reverse("taxi:manufacturer-list")

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
        self.assertRedirects(res, self.url_list)
        self.assertFalse(Manufacturer.objects.filter(
            pk=self.manufacturer.pk
        ).exists())


class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u1", password="p1", license_number="ABC12345"
        )
        cls.m1 = Manufacturer.objects.create(name="Maker A", country="PL")
        cls.m2 = Manufacturer.objects.create(name="Maker B", country="UK")
        for i in range(1, 8):
            Car.objects.create(
                model=f"Model {i}",
                manufacturer=cls.m1 if i <= 4 else cls.m2
            )
        cls.url = reverse("taxi:car-list")

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_ok_and_template(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("object_list", res.context)
        self.assertIn("search_form", res.context)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_paginated(self):
        res = self.client.get(self.url)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertEqual(res.context["paginator"].count, 7)
        self.assertEqual(res.context["page_obj"].number, 1)
        self.assertTrue(res.context["page_obj"].has_next())

    def test_paginate_page_2(self):
        res = self.client.get(self.url, {"page": 2})
        self.assertEqual(res.context["page_obj"].number, 2)
        self.assertTrue(res.context["page_obj"].has_previous())
        self.assertFalse(res.context["page_obj"].has_next())

    def test_queryset_filter_by_model(self):
        res = self.client.get(self.url, {"model": "Model 3"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["paginator"].count, 1)


class PublicCarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="X", manufacturer=cls.m)
        cls.url = reverse("taxi:car-detail", kwargs={"pk": cls.car.pk})

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u2", password="p2", license_number="XYZ99911"
        )
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="X", manufacturer=cls.m)
        cls.url = reverse(
            "taxi:car-detail",
            kwargs={"pk": cls.car.pk}
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_detail_ok(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"].pk, self.car.pk)


# ---------- CAR CREATE / UPDATE / DELETE ----------
class PublicCarCreateUpdateDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="Y", manufacturer=cls.m)
        cls.url_create = reverse("taxi:car-create")
        cls.url_update = reverse("taxi:car-update", kwargs={"pk": cls.car.pk})
        cls.url_delete = reverse("taxi:car-delete", kwargs={"pk": cls.car.pk})

    def test_create_login_required(self):
        self.assertNotEqual(self.client.get(self.url_create).status_code, 200)

    def test_update_login_required(self):
        self.assertNotEqual(self.client.get(self.url_update).status_code, 200)

    def test_delete_login_required(self):
        self.assertNotEqual(self.client.get(self.url_delete).status_code, 200)


class PrivateCarCreateUpdateDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="u3", password="p3", license_number="LIC11122"
        )
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="Z", manufacturer=cls.m)
        cls.url_create = reverse("taxi:car-create")
        cls.url_list = reverse("taxi:car-list")
        cls.url_update = reverse("taxi:car-update", kwargs={"pk": cls.car.pk})
        cls.url_delete = reverse("taxi:car-delete", kwargs={"pk": cls.car.pk})

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_create_has_form(self):
        res = self.client.get(self.url_create)
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_create_car(self):
        data = {"model": "NewCar", "manufacturer": self.m.pk}
        res = self.client.post(self.url_create, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Car.objects.filter(
            model="NewCar",
            manufacturer=self.m
        ).exists())
        self.assertRedirects(res, self.url_list)

    def test_get_update_has_form(self):
        res = self.client.get(self.url_update)
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_update_car(self):
        res = self.client.post(
            self.url_update,
            {"model": "Z-upd", "manufacturer": self.m.pk}
        )
        self.assertRedirects(res, self.url_list)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Z-upd")

    def test_delete_car(self):
        res = self.client.post(self.url_delete, follow=True)
        self.assertRedirects(res, self.url_list)
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())


# ---------- DRIVER LIST / DETAIL ----------
class PublicDriverListDetailViewTest(TestCase):
    def test_list_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("taxi:driver-list")).status_code,
            200
        )

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="pubd", password="p", license_number="L1000001"
        )
        cls.url_detail = reverse(
            "taxi:driver-detail",
            kwargs={"pk": cls.user.pk}
        )

    def test_detail_login_required(self):
        self.assertNotEqual(
            self.client.get(self.url_detail).status_code,
            200
        )


class PrivateDriverListDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="d1",
            password="p1",
            license_number="DL100001"
        )
        # cпочатку створюємо інших
        for i in range(1, 8):
            Driver.objects.create_user(
                username=f"user{i}",
                password="p!",
                license_number=f"TST{(i + 300): 05d}",
                first_name=f"F{i}",
                last_name=f"L{i}",
            )
        # тепер можемо надійно взяти "іншого"
        cls.other = Driver.objects.exclude(
            pk=cls.user.pk
        ).order_by("pk").first()
        assert cls.other is not None, "Need at least two drivers for this test"

        cls.url_list = reverse("taxi:driver-list")
        cls.url_detail = reverse(
            "taxi:driver-detail",
            kwargs={"pk": cls.other.pk}
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_paginated_and_form(self):
        res = self.client.get(self.url_list)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertIn("search_form", res.context)

    def test_list_page_2(self):
        res = self.client.get(self.url_list, {"page": 2})
        self.assertEqual(res.context["page_obj"].number, 2)

    def test_detail_ok(self):
        other = Driver.objects.exclude(pk=self.user.pk).first()
        res = self.client.get(self.url_detail)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["object"].pk, other.pk)

    def test_queryset_filter_username(self):
        res = self.client.get(self.url_list, {"username": "user3"})
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(res.context["paginator"].count, 1)
        self.assertTrue(
            any(u.username == "user3" for u in res.context["object_list"])
        )

        res2 = self.client.get(self.url_list, {"username": "no_such_user"})
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.context["paginator"].count, 0)

        res3 = self.client.get(self.url_list, {"username": ""})
        self.assertEqual(res3.status_code, 200)
        # додатково: порожній запит повертає повний список
        self.assertEqual(
            res3.context["paginator"].count,
            Driver.objects.count()
        )


# ---------- DRIVER CREATE / LICENSE UPDATE / DELETE ----------
class PrivateDriverCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Driver.objects.create_user(
            username="admin", password="p-admin", license_number="ADM00111"
        )
        cls.url_create = reverse("taxi:driver-create")

    def setUp(self):
        self.client.force_login(self.admin)

    def test_get_create_has_form(self):
        res = self.client.get(self.url_create)
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
        res = self.client.post(self.url_create, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Driver.objects.filter(
            username="new_driver_02"
        ).exists())


class PrivateDriverLicenseUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="new_driver_01",
            password="Str0ng-Password!",
            license_number="OLD12345",
        )
        cls.url_update = reverse(
            "taxi:driver-update",
            kwargs={"pk": cls.user.pk}
        )
        cls.url_license_update = reverse(
            "taxi:driver-license-update",
            kwargs={"pk": cls.user.pk}
        )
        cls.url_list = reverse("taxi:driver-list")

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_has_form(self):
        res = self.client.get(self.url_update)
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)

    def test_update_license(self):
        res = self.client.post(
            self.url_license_update,
            {"license_number": "NEW99967"}
        )
        self.assertRedirects(res, self.url_list)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "NEW99967")


class PrivateDriverDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="delme",
            password="p",
            license_number="DEL1234"
        )

    def setUp(self):
        self.client.force_login(self.user)


# ---------- TOGGLE ASSIGN TO CAR ----------
class ToggleAssignToCarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="toggle",
            password="p",
            license_number="TOG1111"
        )
        cls.m = Manufacturer.objects.create(name="Maker", country="PL")
        cls.car = Car.objects.create(model="T", manufacturer=cls.m)
        cls.url_toggle = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": cls.car.pk}
        )
        cls.url_detail = reverse("taxi:car-detail", args=[cls.car.pk])

    def setUp(self):
        self.client.force_login(self.user)

    def test_toggle_add_and_remove(self):
        res = self.client.post(self.url_toggle, follow=True)
        self.assertRedirects(res, self.url_detail)
        self.assertTrue(self.car.drivers.filter(pk=self.user.pk).exists())

        # remove
        res = self.client.post(self.url_toggle, follow=True)
        self.assertRedirects(res, self.url_detail)
        self.assertFalse(self.car.drivers.filter(pk=self.user.pk).exists())
