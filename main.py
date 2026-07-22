from fastapi import FastAPI
import psycopg2 
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection=psycopg2.connect(os.getenv("DATABASE_URL"))


class Student(BaseModel):
    id: int = None
    name: str = None
    course: str = None

#get all students
cursor = connection.cursor()

@app.get("/students")
def get__students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print(rows)

    

    result = []
    for row in rows:
        result.append({
            "id":row[0],
            "name": row[1],
            "course": row[2]

        })
    return result    

#get single students
@app.get("/students/{id}")
def get_single_student(id: int):
    cursor.execute("SELECT * FROM  students WHERE id=%s",(id,))
    row = cursor.fetchone()
    return {
        "id": row[0],
        "name":row[1],
        "course":row[2]
    }

# CREATE NEW STUDET RECORD
@app.post("/students")
def create_student_record(student: Student):
    cursor.execute("INSERT INTO students VALUES(%s,%s,%s)",(student.id,student.name,student.course))
    connection.commit()

    return {
        "message":"Student record created successfully!"
    }
#replace student record
@app.put("/students/{id}")
def replace_student_record(id: int , student: Student):
    cursor.execute("UPDATE students SET id=%s,name=%s, course=%s WHERE id=%s",(student.id,student.name,student.course,id))
    connection.commit()

    return{
        "message":"record replaced successfully"
    }
#update the Student record
@app.patch("/students/{id}")
def update_student_record(id:int,student:Student):
    if student.id != None:
        cursor.execute("UPDATE students SET id=%s WHERE id=%s",(student.id,id))
        connection.commit()
    if student.name != None:
        cursor.execute("UPDATE students SET name=%s WHERE id=%s",(student.name,id))
        connection.commit()
    if student.course != None:
        cursor.execute("UPDATE students SET course=%s WHERE id=%s",(student.course,id))
        connection.commit()

    return{
        "message":"Record updated Successfully"
    }
#perform delete in student record

@app.delete("/students/{id}")
def delete_student_record(id:int):
    cursor.execute("DELETE FROM students WHERE id=%s",(id,))
    connection.commit()

    return{
        "messgae":"record deleted successfully"
    }


