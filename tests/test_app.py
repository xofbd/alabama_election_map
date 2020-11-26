import pytest

from alabama.app.app import app


@pytest.fixture
def test_client():
    with app.test_client() as test_client:
        return test_client


def test_root(test_client):
    """
    GIVEN a Flask application context
    WHEN a GET request is made to '/'
    THEN check that the request was redirected
    """
    response = test_client.get('/')
    assert response.status_code == 302


def test_plot(test_client):
    """
    GIVEN a Flask application context
    WHEN a GET request is made to '/plot'
    THEN check that 200 status code is returned
    """
    response = test_client.get('/plot')
    assert response.status_code == 200
