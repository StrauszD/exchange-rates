import requests

from entities.auth_error import AuthError
from flask import request, _request_ctx_stack
from jose import jwt
from functools import wraps

AUTH0_DOMAIN = 'exchange-rates.us.auth0.com'
API_AUDIENCE = 'https://exchange-rates/api'
ALGORITHMS = ["RS256"]


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)

    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]

    return token


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_token_auth_header()
            url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
            json_url = requests.request('GET', url)
            jwks = json_url.json()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}

            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }

            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer="https://"+AUTH0_DOMAIN+"/"
                    )
                except jwt.ExpiredSignatureError:
                    raise AuthError({"code": "token_expired",
                                    "description": "token is expired"}, 401)
                except jwt.JWTClaimsError:
                    raise AuthError({"code": "invalid_claims",
                                    "description":
                                        "incorrect claims,"
                                        "please check the audience and issuer"}, 401)
                except Exception:
                    raise AuthError({"code": "invalid_header",
                                    "description":
                                        "Unable to parse authentication"
                                        " token."}, 401)

                _request_ctx_stack.top.current_user = payload

                return f(*args, **kwargs)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description": "Unable to find appropriate key"}, 401)

    return decorated
