from pydantic import BaseModel

class LoginUserRequest(BaseModel):

    name: str
    password: str