import pytest

from django.test import Client
from django.db import connections
from django.db.utils import OperationalError

@pytest.fixture(scope='session', autouse=True)
def wait_for_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        db_conn = connections['default']
        try:
            db_conn.cursor()
            print("Fixture-DB: CONNECTED")

        except OperationalError:
            pytest.fail("Database is not available")

@pytest.fixture(scope='session')
def django_client():
    # Инициализация тестового клиента Django
    client = Client()

    print('Fixture-DJANGO-CLIENT: CONNECTED')
    return client

