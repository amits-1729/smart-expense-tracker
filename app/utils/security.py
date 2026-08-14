from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    password = "test123"

    hashed = hash_password(password)

    print("Original:", password)
    print("Hashed:", hashed)
    print("Verified:", verify_password(password, hashed))