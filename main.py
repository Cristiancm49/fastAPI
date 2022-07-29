# Python
from doctest import Example
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import Field 

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File


app = FastAPI()

# Models
class City(Enum):
    buenos_aires= "buenos aires"
    bogota= "bogota"

class State(Enum):
    cundinamarca= "cundinamarca"
    caqueta= "caqueta"

class Country(Enum):
    colombia= "colombia"
    argentina= "argentina"

class HairColor(Enum):
    white= "white"
    black= "black"
    brown= "brown"
    red= "red"
    blonde= "blonde"


class Location(BaseModel):
    city: City = Field(default = None, example="bogota")
    state: State = Field(default = None, example="cundinamarca")
    country: Country = Field(default = None, example="colombia")


class PersonBase(BaseModel):
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
    hair_color: Optional[HairColor] = Field(default = "white")
    is_married: Optional[bool] = Field(default = None) 


class Person(PersonBase):
    
    password: str = Field(..., min_Length=8)


class PersonOut(PersonBase):
   pass


class Config:
    schema_extra = {
        "example":{
            "first_name": "Cristian",
            "last_name": "Cortes Mondragon",
            "age": 21,
                "hair_color": "blonde",
                "is_married": True
            }
        }

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="cristian")

@app.get("/")
def home():
    return {"Hello" : "World"}

@app.post("/person/new", 
    response_model=PersonOut,
    status_code= status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    Esta path opretation crea una persona en la app y guarda la informacion en la base de datos

    Parameters:
    - Request body parameters:
        -**person: Person** -> A person model with first name, last name, age, hair color and marital status
    
    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It is between 1 and 50 chararters",
        example="Andrea"
        ), 
    age: str = Query(
        ..., 
        title="Person Age",
        description="This is the person age. It is required",
        example=42
        )
):
    return {name: age}

# Validaciones # Path operations
persons = [1, 2, 3, 4, 5]
@app.get(
    path="/person/detail/{person_id}",
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person id",
        description="This is the person's id. It is required and must be graater than 0",
        example=45
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'this person does not exist'
        )
    return {person_id: "It exists!"}

# validaciones : request body

@app.put(
    path="/person/{person_id}",
    tags=["Persons"]
    )
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
    
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(...,
        Max_Length=20,
        min_Length=1
    ),
    last_name: str = Form(...,
        Max_Length=20,
        min_Length=1
    ),
    email: EmailStr = Form(...),
        message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str]= Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return{
        'Filename':image.filename,
        'Format': image.content_type,
        'Size(kb)':round(len(image.file.read())/1024, ndigits=2)
    }