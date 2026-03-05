from pydantic import BaseModel


class AppError(BaseModel):
    message: str
    code: int