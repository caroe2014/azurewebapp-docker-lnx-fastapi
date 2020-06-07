from fastapi import FastAPI
from pydantic import BaseModel
#from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
     "http://localhost:5000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user = [{"user": "adam", "job": "global security"},
                 {"user": "Chris", "job": "Blesser of Images"},
                 {"user": "John", "job": "Assistant"}]
#app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

#@app.get("/items/")
#async def read_item(name: str):
#    return fake_items_db[skip : skip + limit]


@app.get("/users/")
async def get_users():
    return user

@app.post("/items/")
async def create_item(item: Item):
    return {"response": "http 200",
             "message": "successful transaction"}