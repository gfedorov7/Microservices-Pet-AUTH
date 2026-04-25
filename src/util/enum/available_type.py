from enum import Enum


class AvailableType(Enum):
    user_signed_up = "user_signed_up"
    user_signed_up_failed = "user_signed_up_failed"
    user_logged_in = "user_logged_in"
    user_login_failed = "user_login_failed"
    user_logged_out = "user_logged_out"
