import jwt
from fastapi import HTTPException, Header

from pydantic import BaseModel
from starlette import status

from src.config.config import settings


def camel_string(snake_str):
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def camelize_dict(snake_dict):
    new_dict = {}
    for key, value in snake_dict.items():
        new_key = camel_string(key)
        if isinstance(value, list):
            new_dict[new_key] = list(map(camelize_dict, value))
        elif isinstance(value, dict):
            new_dict[new_key] = camelize_dict(value)
        else:
            new_dict[new_key] = value
    return new_dict


class CamelModel(BaseModel):
    class Config:
        alias_generator = camel_string
        allow_population_by_field_name = True
        by_alias = True


def decode_token(encoded_token: str):
    try:
        decoded_token = jwt.decode(encoded_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token
    except Exception:
        return {}


def verify_jwt(token: str = Header(...)) -> None:
    authorized = bool(decode_token(token))
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
