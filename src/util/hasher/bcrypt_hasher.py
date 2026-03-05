import bcrypt

from src.util.hasher.hasher import Hasher


class BcryptHasher(Hasher):
    @staticmethod
    def hash(data: any) -> bytes:
        return bcrypt.hashpw(bytes(data), BcryptHasher._get_salt())

    @staticmethod
    def compare(hash_value: bytes, value: any) -> any:
        return bcrypt.checkpw(hash_value, value)

    @staticmethod
    def _get_salt():
        return bcrypt.gensalt()