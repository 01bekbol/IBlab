from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, validator
from typing import List
import uvicorn

app = FastAPI()

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Mount static files (if needed, e.g., for CSS/JS)

# Data model for advanced form submission with validation
class Feedback(BaseModel):
    name: str
    email: EmailStr
    message: str
    tags: List[str]

    @validator("message")
    def validate_message_length(cls, value):
        if len(value) < 10:
            raise ValueError("Message must be at least 10 characters long.")
        return value

# Home route with a form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Complex form submission route 1
@app.post("/submit")
async def submit_sform(
    name: str = Form(...), 
    email: str = Form(...), 
    message: str = Form(...), 
    tags: List[str] = Form(...)):
    # Validate message length
    if len(message) < 10:
        raise HTTPException(status_code=400, detail="Message must be at least 10 characters long.")
    # Process the form data
    data = {
        "name": name,
        "email": email,
        "message": message,
        "tags": tags
    }
    return JSONResponse(content={"message": "Form submitted successfully!", "data": data})

# Complex JSON submission route 2
@app.post("/submit-json")
async def submit_json(data: Feedback):
    # Perform advanced data processing, such as saving to a database
    processed_data = data.dict()
    processed_data["tags"] = [tag.upper() for tag in processed_data["tags"]]
    return JSONResponse(content={"message": "JSON submitted successfully!", "processed_data": processed_data})