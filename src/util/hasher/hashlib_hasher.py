import hashlib
import hmac

from src.util.hasher.bcrypt_hasher import BcryptHasher
from src.util.hasher.hasher import Hasher


class HashlibHasher(Hasher):
    @staticmethod
    def hash(data: str) -> bytes | str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def compare(hash_value: bytes | str, value: str) -> bool:
        hsh = BcryptHasher.hash(value)
        return hmac.compare_digest(hsh, hash_value)
