from functools import wraps
from flask import request

from entities.auth_error import AuthError
from entities.rate_limit_error import RateLimitError
from services.redis_service import RedisService

redis = RedisService()


def get_user_header():
    user = request.headers.get('User', None)

    if not user:
        raise AuthError(
            {
                'code': 'user_header_missing',
                'description': 'User header is expected'
             },
            401
        )

    return user


def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user = get_user_header()

            if redis.exists(user):
                requests = int(redis.get(user).decode('utf-8'))
                if requests <= 15:
                    redis.set(user, requests + 1, 180)
                else:
                    raise RateLimitError(
                        {
                            'code': 'rate limit error',
                            'description': 'User has exceeded API rate limit'
                        },
                        403
                    )
            else:
                redis.set(user, 1, 180)

            return f(*args, **kwargs)
        except RateLimitError:
            raise RateLimitError(
                {
                    'code': 'rate limit error',
                    'description': 'User has exceeded API rate limit'
                },
                403
            )
        except AuthError:
            raise AuthError(
                {
                    'code': 'user_header_missing',
                    'description': 'User header is expected'
                },
                401
            )
        except Exception:
            raise RateLimitError(
                {
                    'code': 'rate limit error',
                    'description': 'Error getting user calls'
                },
                403
            )

    return decorated
