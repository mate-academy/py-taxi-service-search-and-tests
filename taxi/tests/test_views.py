import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from taxi.models import Manufacturer, Car


# Yeah, this parametrization does not look pretty at all.
@pytest.mark.parametrize(
    "url",
    {
        pytest.param(
            reverse("taxi:index"),
            id="index page should not be accessible for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:manufacturer-list"),
            id="Manufacturer list page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:manufacturer-create"),
            id="Manufacturer creation page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:manufacturer-update", args=[1]),
            id="Manufacturer update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:manufacturer-delete", args=[1]),
            id="Manufacturer delete page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:car-list"),
            id="Car list page should not be accessible for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:car-detail", args=[1]),
            id="Car detail page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:car-update", args=[1]),
            id="Car update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:car-delete", args=[1]),
            id="Car delete page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:car-create"),
            id="Car create page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:toggle-car-assign", args=[1]),
            id="Car assignment view should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:driver-list"),
            id="Driver list page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:driver-detail", args=[1]),
            id="Driver detail page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:driver-create"),
            id="Driver create page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:driver-update", args=[1]),
            id="Driver update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("taxi:driver-delete", args=[1]),
            id="Driver delete page should not be accessible "
            "for unauthorized users",
        ),
    },
)
def test_login_required(url, client):
    # This test will also fail if the database is accessed during test.
    # Therefore, its behaviour definitely should be changed if
    # at some point there appear pages that allow database access to
    # unauthorized users. :)
    assert client.get(url).status_code == 302


class TestManufacturerViews:
    @pytest.mark.django_db
    def test_manufacturer_list(self, manufacturers_data, driver_client):
        response = driver_client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()

        assert response.status_code == 200
        assert list(response.context["manufacturer_list"]) == list(
            manufacturers
        )

    @pytest.mark.django_db
    def test_manufacturer_template(self, driver_client):
        response = driver_client.get(reverse("taxi:manufacturer-list"))

        assertTemplateUsed(response, "taxi/manufacturer_list.html")

    @pytest.mark.django_db
    def test_create_manufacturer(self, driver_client):
        form_data = {"name": "Toyota", "country": "Japan"}

        response = driver_client.post(
            reverse("taxi:manufacturer-create"), data=form_data
        )

        manufacturer = Manufacturer.objects.get(name=form_data["name"])

        assert response.status_code == 302
        assert manufacturer.country == form_data["country"]

    @pytest.mark.django_db
    def test_update_manufacturer(self, driver_client, manufacturers_data):
        form_data = {"name": "Lincoln", "country": "USA"}
        entry_id = 1

        response = driver_client.post(
            reverse("taxi:manufacturer-update", args=[entry_id]),
            data=form_data,
        )

        manufacturer = Manufacturer.objects.get(pk=entry_id)

        assert response.status_code == 302
        assert manufacturer.name == form_data["name"]
        assert manufacturer.country == form_data["country"]

    @pytest.mark.django_db
    def test_delete_manufacturer(self, driver_client, manufacturers_data):
        entry_id = 1

        response = driver_client.post(
            reverse("taxi:manufacturer-delete", args=[entry_id])
        )

        assert response.status_code == 302
        assert not Manufacturer.objects.filter(pk=entry_id).exists()

    @pytest.mark.django_db
    def test_search_manufacturer(self, driver_client, manufacturers_data):
        # Probably not how you do it.
        response = driver_client.get(
            reverse("taxi:manufacturer-list") + "?name=y"
        )
        manufacturers = Manufacturer.objects.filter(name__icontains="y")

        assert list(response.context["manufacturer_list"]) == list(
            manufacturers
        )


class TestDriverViews:
    @pytest.mark.django_db
    def test_driver_list(self, drivers_data, driver_client):
        response = driver_client.get(reverse("taxi:driver-list"))
        drivers = get_user_model().objects.all()

        assert response.status_code == 200
        assert list(response.context["driver_list"]) == list(drivers)

    @pytest.mark.django_db
    def test_car_template(self, driver_client):
        response = driver_client.get(reverse("taxi:driver-list"))

        assertTemplateUsed(response, "taxi/driver_list.html")

    @pytest.mark.django_db
    def test_create_driver(self, driver_client):
        form_data = {
            "username": "test.user",
            "password1": "zLjyFH7qd1icr33e",
            "password2": "zLjyFH7qd1icr33e",
            "first_name": "Test",
            "last_name": "One",
            "license_number": "ADD23345",
        }

        response = driver_client.post(
            reverse("taxi:driver-create"), data=form_data
        )

        driver = get_user_model().objects.get(username=form_data["username"])

        assert response.status_code == 302
        assert driver.license_number == form_data["license_number"]
        assert driver.first_name == form_data["first_name"]
        assert driver.last_name == form_data["last_name"]
        assert driver.check_password(form_data["password1"])

    @pytest.mark.django_db
    def test_update_driver(self, drivers_data, driver_client):
        form_data = {"license_number": "ADZ23345"}
        driver_id = 1

        response = driver_client.post(
            reverse("taxi:driver-update", args=[driver_id]), data=form_data
        )

        driver = get_user_model().objects.get(pk=driver_id)

        assert response.status_code == 302
        assert driver.license_number == form_data["license_number"]

    @pytest.mark.django_db
    def test_delete_driver(self, driver_client):
        driver_id = 1

        response = driver_client.post(
            reverse("taxi:driver-delete", args=[driver_id])
        )

        assert response.status_code == 302
        assert not get_user_model().objects.filter(pk=driver_id).exists()

    @pytest.mark.django_db
    def test_search_driver(self, driver_client, drivers_data):
        # Probably not how you do it 2.
        response = driver_client.get(
            reverse("taxi:driver-list") + "?username=one"
        )
        drivers = get_user_model().objects.filter(username__icontains="one")

        assert list(response.context["driver_list"]) == list(drivers)


class TestCarViews:
    @pytest.mark.django_db
    def test_car_list(
        self, manufacturers_data, drivers_data, cars_data, driver_client
    ):
        response = driver_client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        assert response.status_code == 200
        assert list(response.context["car_list"]) == list(cars)

        assertTemplateUsed(response, "taxi/car_list.html")

    @pytest.mark.django_db
    def test_manufacturer_template(self, driver_client):
        response = driver_client.get(reverse("taxi:car-list"))

        assertTemplateUsed(response, "taxi/car_list.html")

    @pytest.mark.django_db
    def test_create_car(self, manufacturers_data, drivers_data, driver_client):
        form_data = {
            "model": "Test Model 1",
            "manufacturer": 1,
            "drivers": [1, 2],
        }

        response = driver_client.post(
            reverse("taxi:car-create"), data=form_data
        )

        car = Car.objects.get(model=form_data["model"])

        assert response.status_code == 302
        assert car.model == form_data["model"]
        assert car.manufacturer.id == form_data["manufacturer"]
        assert [driver.id for driver in car.drivers.all()] == form_data[
            "drivers"
        ]

    @pytest.mark.django_db
    def test_update_car(
        self, drivers_data, manufacturers_data, cars_data, driver_client
    ):
        form_data = {
            "model": "Test Model 1",
            "manufacturer": 2,
            "drivers": 3,
        }
        car_id = 1

        response = driver_client.post(
            reverse("taxi:car-update", args=[car_id]), data=form_data
        )

        car = Car.objects.get(pk=car_id)

        assert response.status_code == 302
        assert car.model == form_data["model"]
        assert car.manufacturer.id == form_data["manufacturer"]
        assert car.drivers.get().id == form_data["drivers"]

    @pytest.mark.django_db
    def test_delete_car(
        self, drivers_data, manufacturers_data, cars_data, driver_client
    ):
        car_id = 1

        response = driver_client.post(
            reverse("taxi:car-delete", args=[car_id])
        )

        assert response.status_code == 302
        assert not Car.objects.filter(pk=car_id).exists()

    @pytest.mark.django_db
    def test_search_cars(
        self, drivers_data, manufacturers_data, cars_data, driver_client
    ):
        # Probably not how you do it 3.
        response = driver_client.get(
            reverse("taxi:car-list") + "?model=5"
        )
        cars = Car.objects.filter(model__icontains="5")

        assert list(response.context["car_list"]) == list(
            cars
        )
