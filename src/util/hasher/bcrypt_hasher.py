from typing import Any

import bcrypt

from src.util.hasher.hasher import Hasher


class BcryptHasher(Hasher):
    @staticmethod
    def hash(data: Any) -> bytes | str:
        return bcrypt.hashpw(data.encode(), BcryptHasher._get_salt())

    @staticmethod
    def compare(hash_value: bytes | str, value: str) -> bool:
        return bcrypt.checkpw(value.encode(), hash_value)

    @staticmethod
    def _get_salt():
        return bcrypt.gensalt()