
from fastapi import FastAPI, HTTPException, Body
import uvicorn
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

# user = {"id" : 1, "name" : "mgmg", "email" : "mgmg.gmail.com", "age": 5, "bio" : "study cs", "role": "student", "password" : "12345"}

# print(user['name'])

class UserCreate(BaseModel):
	id: int = Field(..., gt=0, description="User ID", examples=[1])
	name: str = Field(..., min_length=3, max_length=50, description="User Name", examples=["Mg Mg"])
	email: EmailStr = Field(...,description="Email Address", examples=["mg@gmail.com"])
	age: int = Field(..., ge=18, le=100, description="Age", examples=[20])
	bio: str | None = Field(default=None, max_length=200, description="Biography")
	role : str
	password : str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    bio: str | None = None

# u1 = UserCreate(id=1, name="mgmg", email="mgmg@gmail.com", age=18, role='student', password='12345')
# print(u1)
# print(u1.name)
# print(u1.email)
# u2 = UserCreate(id=1, name="mgmg", email="mgmg@gmail.com", age=18, role='student', password='12345')
# print(u2.name)
# print("end program...")

data_users = []

app = FastAPI(title="Upamar - 3", version="1.0")

@app.get("/")
def home():
	return {"message" : "Mingalarpar"}

@app.get("/users", response_model=list[UserResponse])
def get_users():
	return data_users

@app.post("/users/add", response_model=UserResponse)
def add_user(user: Annotated[UserCreate, Body(..., description="Create New User")]):
	data_users.append(user)
	# return {"message" : "ok"}
	return user

if __name__ == "__main__":
    uvicorn.run("upamar_3:app", host="127.0.0.1", port=8000, reload=True)

