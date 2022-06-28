# Python

from typing import Optional
from enum import Enum


# Pydantic
from pydantic import BaseModel
from pydantic import Field 

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()

# Models
class HairColor(Enum):
    white: "white"
    black: "black"
    brown: "brown"
    red: "red"
    blonde: "blonde"


class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=100
    )
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)



@app.get("/")
def home():
    return {"Hello" : "World"}

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It is between 1 and 50 chararters",
        ), 
    age: str = Query(
        ..., 
        title="Person Age",
        description="This is the person age. It is required",
        )
):
    return {name: age}

# Validaciones # Path operations

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person id",
        description="This is the person's id. It is required and must be graater than 0"
        )
):
    return {person_id: "It exists!"}

# validaciones : request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is person ID. It is required.',
        gt= 0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
