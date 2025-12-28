def test_search_drivers(client):
    response = client.get("/search/drivers?q=John")
    assert response.status_code == 200
    assert response.get_json() == [
        {"username": "John",}
    ]

def test_search_cars(client):
    response = client.get("/search/cars?q=Toyota")
    assert response.status_code == 200
    assert response.get_json() == [
        {"model": "Toyota",}
    ]

def test_search_manufacturer(client):
    response = client.get("/search/manufacturers?q=ford")
    assert response.status_code == 200
    assert response.get_json() == [
        {"name": "ford",}
    ]

