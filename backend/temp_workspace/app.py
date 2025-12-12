from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sqlite3

app = FastAPI()

class Employee(BaseModel):
    name: str
    email: str
    role: str

@app.post("/register")
async def register(name: str = Form(...), email: str = Form(...), role: str = Form(...)):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, email, role) VALUES (?, ?, ?)", (name, email, role))
        conn.commit()
        conn.close()
        return JSONResponse(content={"success": True}, media_type="application/json")
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, media_type="application/json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)