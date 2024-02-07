from uuid import uuid4
from pytest import fixture


@fixture(scope="function")
def authentication_headers():
    return {
        "Authorization": f"Bearer {uuid4()}",
    }


@fixture(scope="function")
def firebase_invalid_id_token(authentication_headers):
    invalid_id_token = 123
    authentication_headers["Authorization"] = f"Bearer {invalid_id_token}"
    return authentication_headers
