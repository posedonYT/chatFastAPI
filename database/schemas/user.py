from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserResponseSchema(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=14, le=120)

class NewUserSchema(UserResponseSchema):
    password: str = Field(min_length=6)

    model_config = ConfigDict(extra="forbid")

class UserSchema(NewUserSchema):
    id: int = Field()
