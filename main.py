from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr

from fastapi import (
    status,
    Body,
    Cookie,
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    UploadFile,
)

app = FastAPI()


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The city where the person lives",
        example="New York",
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The state where the person lives",
        example="New York",
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The country where the person lives",
        example="United States",
    )


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Miguel")
    last_name: str = Field(..., min_length=1, max_length=50, example="Gonzalez")
    age: int = Field(..., gt=0, le=115, example=25)
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.brown)
    is_married: Optional[bool] = Field(default=None, example=False)


class Person(PersonBase):
    password: str = Field(..., min_length=8, example="mipassword")


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguelzetina")
    message: str = Field(default="Login successfully")


@app.get("/")
def home():
    return {"Hello": "World!"}


@app.post(
    path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person


@app.get("/person/detail")
def show_person(
    name: str = Query(
        ...,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name,  It's between 1 and 50 characters",
        example="Rocio",
    ),
    age: Optional[str] = Query(
        None,
        title="Person Age",
        description="This is the person age, It's required",
        example="25",
    ),
):
    return {name: age}


@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0, example=123)):
    if person_id not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡Person doesn't exists!"
        )
    return {person_id: "It exists!"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., title="Person ID", description="This is the person ID", gt=0, example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    return person


@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


@app.post(path="/contact", status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(..., max_length=20, min_length=1),
    last_name: str = Form(..., max_length=20, min_length=1),
    email: EmailStr = Form(...),
    message: str = Form(..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent


@app.post(path="/post-image")
def post_image(image: UploadFile = File(...)):
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size": round(len(image.file.read()) / 1024, ndigits=2),
    }
