
from fastapi import FastAPI, HTTPException, Body
import uvicorn
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

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

class UserUpdate(BaseModel):
	name: str = Field(..., min_length=3, max_length=50, description="User Name", examples=["Mg Mg"])
	email: EmailStr = Field(...,description="Email Address", examples=["mg@gmail.com"])
	age: int = Field(..., ge=18, le=100, description="Age", examples=[20])
	bio: str | None = Field(default=None, max_length=200, description="Biography")
	role : str


data_users : list[UserCreate] = []

app = FastAPI(title="Upamar - 4", version="1.0")

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

@app.put("/users/{user_id}", response_model=UserResponse, summary="အချက်အလက်အားလုံး ပြင်ခြင်း")
def update_complete(user_id: int, update_user : UserCreate):
	for index, existing_user in enumerate(data_users):
		if existing_user.id == user_id:
			data_users[index] = update_user
			return update_user

	raise HTTPException(status_code = 404, detail="User not found with this id")


@app.patch("/users/{user_id}", response_model=UserResponse, summary="ပြောင်းလဲချင်တဲ့ အချက်အလက်ကိုပဲ ရွေးပြင်ခြင်း")
def update_user_partial(user_id: int, patch_data: UserUpdate):
	for existing_user in data_users:
		if existing_user.id == user_id:
			update_dict = patch_data.model_dump(exclude_unset=True)
			
			for key, value in update_dict.items():
				setattr(existing_user, key, value)
				
			return existing_user
			
	raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
	for index, existing_user in enumerate(data_users):
		if existing_user.id == user_id:
			data_users.pop(index)
			return {"message": f"User with ID {user_id} has been deleted successfully"}
			
	raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")


if __name__ == "__main__":
	uvicorn.run("upamar_4:app", host="127.0.0.1", port=8000, reload=True)

