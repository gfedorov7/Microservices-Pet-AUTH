TOKEN_EXPIRED = "token_expired"
TOKEN_INVALID = "token_invalid"

app_errors = {
    TOKEN_EXPIRED: {
        "message": "Token already expired",
        "code": 401,
    },
    TOKEN_INVALID: {
        "message": "Invalid token",
        "code": 401,
    }
}