from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(password: str, pass_hash: str) -> bool:
    
    return CRIPTO.verify(password, pass_hash)

def generate_hash(password: str) -> str:

    return CRIPTO.hash(password)