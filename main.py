from fastapi import FastAPI, HTTPException
from database import get_db_connection
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()
app = FastAPI()

class Student(BaseModel):
    name: str
    age: int


@app.get("/")
def read_root():
    return {"Hello": os.getenv("HOLA_MUNDO")}


@app.get("/students")
def read_students():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return {"students": students}


@app.post("/students")
def create_student(student: Student):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO students (name, age)
            VALUES (%s, %s)
            RETURNING id, name, age;
            """,
            (student.name, student.age)
        )
        new_student = cursor.fetchone()
        db.commit()
        return {
            "message": "Student added successfully",
            "student": new_student
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inserting student: {str(e)}"
        )
    finally:
        cursor.close()
        db.close()
