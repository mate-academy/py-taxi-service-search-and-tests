import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.parametrize(
    "url",
    [
        pytest.param(
            reverse("taxi:index"),
            id="user must be loggined in to have access to home page"
        ),
        pytest.param(
            reverse("taxi:manufacturer-list"),
            id="user must be loggined in to have access to manufacturer list page"
        ),
        pytest.param(
            reverse("taxi:manufacturer-create"),
            id="user must be loggined in to be able to create manufacturers"
        ),
        pytest.param(
            reverse("taxi:manufacturer-update", args=[1]),
            id="user must be loggined in to be able to update manufacturers"
        ),
        pytest.param(
            reverse("taxi:manufacturer-delete", args=[1]),
            id="user must be loggined in to be able to delete manufacturers"
        ),
        pytest.param(
            reverse("taxi:car-list"),
            id="user must be loggined in to have access to car list page"
        ),
        pytest.param(
            reverse("taxi:car-detail", args=[1]),
            id="user must be loggined in to have access to car detail page"
        ),
        pytest.param(
            reverse("taxi:car-create"),
            id="user must be loggined in to be able to create new car"
        ),
        pytest.param(
            reverse("taxi:car-update", args=[1]),
            id="user must be loggined in to be able to update cars"
        ),
        pytest.param(
            reverse("taxi:car-delete", args=[1]),
            id="user must be loggined in to be able to delete cars"
        ),
        pytest.param(
            reverse("taxi:toggle-car-assign", args=[1]),
            id="user must be loggined in to be able to assign cars"
        ),
        pytest.param(
            reverse("taxi:driver-list"),
            id="user must be loggined in to have access to driver list page"
        ),
        pytest.param(
            reverse("taxi:car-detail", args=[1]),
            id="user must be loggined in to have access to driver detail page"
        ),
        pytest.param(
            reverse("taxi:driver-create"),
            id="user must be loggined in to be able to create new drivers"
        ),
        pytest.param(
            reverse("taxi:driver-update", args=[1]),
            id="user must be loggined in to be able to update drivers"
        ),
        pytest.param(
            reverse("taxi:driver-delete", args=[1]),
            id="user must be loggined in to be able to delete drivers"
        ),
    ]
)
def test_login_required(url, client):
    res = client.get(url)
    assert res.status_code != 200


