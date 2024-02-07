from firebase_admin import auth

from fastapi import Depends
from fastapi import Response
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from app.exceptions import InvalidIdTokenError
from app.exceptions import ExpiredIdTokenError
from app.exceptions import BearerAuthenticationRequiredError


def firebase_authentication(
    res: Response,
    cred: HTTPAuthorizationCredentials = Depends(
        HTTPBearer(auto_error=False)
    )
) -> dict[str, str]:
    if cred is None:
        raise BearerAuthenticationRequiredError()
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except auth.ExpiredIdTokenError:
        raise ExpiredIdTokenError("The provided ID Token has expired.")
    except auth.InvalidIdTokenError:
        raise InvalidIdTokenError("The provided ID Token is not valid.")
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token['user_id']
