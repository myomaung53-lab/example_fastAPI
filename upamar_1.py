
from fastapi import FastAPI

app = FastAPI()

all_users = [
	{"id": 1, "name":"mgmg", "email":"mgmg@gmail.com", "bio":"student"},
	{"id": 2, "name":"koko", "email":"koko@gmail.com", "bio":"teacher"}
]

@app.get("/")
async def welcome() -> dict:
	return {"message": "Hello world"}

@app.get("/users")
async def get_users() -> list:
	return all_users

@app.get("/users/{myid}") # path parameter
async def get_user(myid: int) -> dict:
	for user in all_users:
		if user["id"] == myid:
			return user

	return {"info" : "user not found"}