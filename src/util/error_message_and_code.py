TOKEN_EXPIRED = "Token expired"
TOKEN_INVALID = "Token invalid"

PASSWORD_SHORT = "Password short"
PASSWORD_HAS_NOT_SPEC = "Password has not spec"
PASSWORD_HAS_NOT_NUMBERS = "Password has not numbers"
PASSWORD_HAS_NOT_LETTERS = "Password has not letters"

LOGIN_ALREADY_USED = "Login already used"

app_errors = {
    TOKEN_EXPIRED: {
        "message": "Token already expired",
        "code": 401,
    },
    TOKEN_INVALID: {
        "message": "Invalid token",
        "code": 401,
    },

    PASSWORD_SHORT: {
        "message": "The password is too short",
        "code": 400,
    },
    PASSWORD_HAS_NOT_SPEC: {
        "message": "The password does not contain any special characters",
        "code": 400,
    },
    PASSWORD_HAS_NOT_NUMBERS: {
        "message": "The password does not contain numbers",
        "code": 400,
    },
    PASSWORD_HAS_NOT_LETTERS: {
        "message": "The password does not contain letter",
        "code": 400,
    },

    LOGIN_ALREADY_USED: {
        "message": "Login is already use another user",
        "code": 409,
    },
}