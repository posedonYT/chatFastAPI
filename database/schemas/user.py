from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError

class UserResponseSchema(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=14, le=120)

class NewUserSchema(UserResponseSchema):
    password: str = Field(min_length=6)

    model_config = ConfigDict(extra="forbid")

class UserSchema(NewUserSchema):
    id: int = Field()

class UserLoginRequestSchema(BaseModel):
    identifier: str = Field(min_length=1)
    password: str = Field(min_length=6)
    
    model_config = ConfigDict(extra="forbid")
    
    @field_validator('identifier')
    def validate_identifier(cls, v: str) -> str:
        try:
            from pydantic import validate_email
            validate_email(v)
            return v
        except (ValueError, PydanticCustomError):
            pass
        
        if len(v) > 20:
            raise ValueError(
                "Identifier must be a valid email "
                "or a login with 1-20 characters"
            )
        return v
