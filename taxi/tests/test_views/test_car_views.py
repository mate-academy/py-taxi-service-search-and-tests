from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm, CarForm
from taxi.models import Car


class PublicCarViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def test_login_required_protection_list(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_detail(self):
        url = reverse("taxi:car-detail", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_car_update(self):
        url = reverse("taxi:car-update", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_car_delete(self):
        url = reverse("taxi:car-delete", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[2])
CAR_UPDATE_URL = reverse("taxi:car-update", args=[2])
CAR_DELETE_URL = reverse("taxi:car-delete", args=[2])
CAR_CREATE_URL = reverse("taxi:car-create")
PAGINATION = 5


class PrivateCarViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(id=2)
        self.client.force_login(self.user)
        self.car = Car.objects.get(id=2)

    """Tests for the ListView"""

    def test_list_correct_pagination_content_listed(self):
        url = CAR_LIST_URL
        res = self.client.get(url)
        self.assertEquals(
            list(Car.objects.all()[:PAGINATION]),
            list(res.context.get("car_list")),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_list_create_button_exists(self):
        url = CAR_LIST_URL
        res = self.client.get(url)
        self.assertContains(
            res,
            """a href="/cars/create/" """
            "",
        )

    def test_list_searchbar_exists(self):
        url = CAR_LIST_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("search_form"), CarSearchForm)
        )

    def test_list_search_bar_works(self):
        url = CAR_LIST_URL
        form = CarSearchForm(data={"model": "or"})
        res = self.client.get(url, form.data)
        self.assertTrue(form.is_valid())
        self.assertEquals(
            list(res.context.get("car_list")),
            list(Car.objects.filter(model__icontains="or")[:PAGINATION]),
        )
        self.assertEquals(
            res.context.get("search_form").initial.get("model"), "or"
        )

    def test_list_pagination_does_not_break_search(self):
        url = CAR_LIST_URL
        res = self.client.get(url, data={"model": "a", "page": 2})
        self.assertEquals(
            list(res.context.get("car_list")),
            list(Car.objects.filter(model__icontains="a")[PAGINATION:]),
        )

    """Tests for the DetailView"""

    def test_detail_correct_car(self):
        url = CAR_DETAIL_URL
        res = self.client.get(url)
        self.assertEquals(res.context.get("car"), self.car)

    def test_detail_correct_content(self):
        url = CAR_DETAIL_URL
        res = self.client.get(url)
        self.assertContains(res, self.car.model)
        self.assertContains(res, self.car.manufacturer.name)
        self.assertContains(res, self.car.drivers.last().username)

    def test_detail_correct_links(self):
        url = CAR_DETAIL_URL
        res = self.client.get(url)
        self.assertContains(res, "/cars/2/toggle-assign/")
        self.assertContains(res, "/cars/2/delete/")
        self.assertContains(res, "/cars/2/update/")

    """Tests for the DeleteView"""

    def test_delete_correct_template_name(self):
        url = CAR_DELETE_URL
        res = self.client.get(url)
        self.assertTemplateUsed(res, "taxi/car_confirm_delete.html")

    def test_delete_correct_success_url(self):
        user = get_user_model().objects.create_user(
            username="testo2423rado",
            password="fafeafa4342@",
            license_number="QWS32565",
        )
        self.client.force_login(user)
        url = CAR_DELETE_URL
        res = self.client.post(url)
        self.assertRedirects(res, CAR_LIST_URL)

    """Tests for the CreateView"""

    def test_create_correct_form(self):
        url = CAR_CREATE_URL
        res = self.client.get(url)
        self.assertTrue(isinstance(res.context.get("form"), CarForm))

    def test_create_correct_success_url(self):
        url = CAR_CREATE_URL
        res = self.client.post(
            url, data={"model": "test", "manufacturer": 2, "drivers": 2}
        )
        self.assertRedirects(res, CAR_LIST_URL)

    """Tests for the UpdateView"""

    def test_update_correct_form(self):
        url = CAR_UPDATE_URL
        res = self.client.get(url)
        self.assertTrue(isinstance(res.context.get("form"), CarForm))

    def test_update_correct_success_url(self):
        url = CAR_UPDATE_URL
        res = self.client.post(
            url, data={"model": "test", "manufacturer": 1, "drivers": 1}
        )
        self.assertRedirects(res, CAR_LIST_URL)
