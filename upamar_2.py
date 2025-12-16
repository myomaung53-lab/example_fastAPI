
from fastapi import FastAPI

app = FastAPI()

all_users = [
	{"id": 1, "name":"mgmg", "email":"mgmg@gmail.com", "bio":"student"},
	{"id": 2, "name":"koko", "email":"koko@gmail.com", "bio":"teacher"},
	{"id": 3, "name":"mgmg", "email":"mgmg@gmail.com", "bio":"engineer"},
	{"id": 4, "name":"နေလင်း", "email":"mgmg@gmail.com", "bio":"student"},
	{"id": 5, "name":"ထက်ကို", "email":"koko@gmail.com", "bio":"teacher"},
	{"id": 6, "name":"ဦးကောင်း", "email":"mgmg@gmail.com", "bio":"engineer"},
	{"id": 7, "name":"ဦးချစ်", "email":"mgmg@gmail.com", "bio":"student"},
	{"id": 8, "name":"ဦးမြင့်", "email":"koko@gmail.com", "bio":"teacher"},
	{"id": 9, "name":"မောင်ချစ်", "email":"mgmg@gmail.com", "bio":"engineer"},
	{"id": 10, "name":"မောင်ဇော်", "email":"mgmg@gmail.com", "bio":"student"},

]

@app.get("/")
async def welcome() -> dict:
	return {"message": "Hello world"}

@app.get("/users")
async def get_users(page: int) -> list:
	# return all_users
	size = 3
	start = (page - 1) * size
	end = start + size

	users = all_users[start:end]

	return users


@app.get("/users/{myid}") # path parameter
async def get_user(myid: int) -> dict:
	for user in all_users:
		if user["id"] == myid:
			return user
	return {"info" : "user not found"}

@app.get("/find")
async def find(user_id: int) -> dict:
	for user in all_users:
		if user['id'] == user_id:
			return user

	return {"info" : "user not found"}

@app.get("/search")
async def search(my_name: str, my_bio:str) -> dict:
	for user in all_users:
		if user["name"] == my_name and user['bio'] == my_bio:
			return user

	return {"info" : "user not found"}


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("upamar_2:app", reload=True)