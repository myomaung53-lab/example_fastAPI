
""" sqlite, sqlalchemy, aiosqlite တို့ကိုအသုံးပြုပြီး fastapi မှာ database တည်ဆောက်ခြင်းနဲ့ ချိတ်ဆက်ခြင်း """

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import select



DATABASE_URL = "sqlite+aiosqlite:///./student.db"


engine = create_async_engine(DATABASE_URL, echo=True)

new_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
	pass


class Student(Base):
	__tablename__ = "student.db"

	id : Mapped[int] = mapped_column(primary_key=True)

	name : Mapped[str] = mapped_column(String(100), nullable=False)


	age : Mapped[int] = mapped_column(nullable=False)

	email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class StudentCreate(BaseModel):
	name : str = Field(min_length=2, max_length=100)
	age: int = Field(ge=1, le=120)
	email : str = Field(max_length=100)


class StudentRespone(BaseModel):
	id: int
	name : str
	age : int
	email : str



@asynccontextmanager
async def lifespan(app : FastAPI):
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

	yield


	await engine.dispose()


app = FastAPI(title="database in fastapi", lifespan=lifespan)

@app.get("/")
def home():
	return {"message" : "server is running...."}


@app.post("/students/", response_model=StudentRespone, status_code=201)
async def create_student(data: StudentCreate):
	async with new_session() as db:
		ans = data.model_dump() # {'name': 'mgmg1', 'age': 1, 'email': 'mgmg1@gmail.com'}
		print(ans)
		student = Student(**data.model_dump())
		db.add(student)

		try:
			await db.commit()
		except IntegrityError:
			await db.rollback()
			raise HTTPException(status_code=409, detail="Email already exists")

		return student

@app.get("/students/", response_model=list[StudentRespone])
async def get_students():
	async with new_session() as db:
		result = await db.scalars(select(Student).order_by(Student.id))
		print("result = ", result)

		return result.all()

@app.get("/students/{student_id}", response_model=StudentRespone)
async def get_student(student_id : int):
	async with new_session() as db:
		student = await db.get(Student, student_id)
		print("result by one = ", student)

		if student is None:
			raise HTTPException(status_code=404, detail="Student not found")

		return student

if __name__ == "__main__":
	import uvicorn
	uvicorn.run("upamar_7:app", reload=True)





