from fastapi import FastAPI
from database import get_db_connection
from dotenv import load_dotenv
import os 

load_dotenv()
app = FastAPI()


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