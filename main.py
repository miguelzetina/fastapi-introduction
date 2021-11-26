from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import Body, FastAPI, Path, Query

app = FastAPI()

# Models


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


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Miguel")
    last_name: str = Field(..., min_length=1, max_length=50, example="Gonzalez")
    age: int = Field(..., gt=0, le=115, example=25)
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.brown)
    is_married: Optional[bool] = Field(default=None, example=False)


@app.get("/")
def home():
    return {"Hello": "World!"}


@app.post("/person/new")
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
