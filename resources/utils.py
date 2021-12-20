from passlib.apps import custom_app_context as pwd_context


def pwd_encrypt(plain_pwd: str):
    return pwd_context.encrypt(plain_pwd)


def pwd_verify(plain_pwd: str, encrypt_pwd: str):
    return pwd_context.verify(plain_pwd, encrypt_pwd)