import email
import os
import re
from sre_constants import SUCCESS
import sys

from tkinter import E
from click import password_option
from fastapi import Depends, FastAPI, Form, File, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta
from typing import Optional, List

fpath = os.path.join(os.path.dirname(__file__), 'db')
sys.path.append(fpath)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    email: str
    UID: str
    type: str

class LoginData(BaseModel):
    # remember: bool
    email: str
    password: str
    # remember_me: str

class RegisterData(BaseModel):
    email: str
    password: str

class QuestionData(BaseModel):
    Qname: str
    Scope: str
    Description: str
    Type: str

class UpdateQuestionData(BaseModel):
    SolutionSeq: str
class SolutionData(BaseModel):
    Sname: str
    Type: str
    QID: str

@app.get("/api/")
async def root():
    return {"message": "Hello World"}

@app.post('/api/login_check/')
async def login(loginData: LoginData):
    from db.database import login_check
    return login_check(loginData.email, loginData.password)

@app.post('/api/register/')
def register(registerData: RegisterData):
    from db.database import create_account
    return create_account(registerData.email.split('@')[0], registerData.email, registerData.password, 'user')

@app.post('/api/question/create')
def create_question(questionData: QuestionData):
    from db.database import create_question_prototype
    return create_question_prototype(questionData.Qname, questionData.Scope, questionData.Description, questionData.Type)

@app.post('/api/question/update/{QID}')
def update_question(QID: str, updateQuestionData: UpdateQuestionData):
    from db.database import update_question_prototype
    return update_question_prototype(QID, updateQuestionData.SolutionSeq)

@app.post('/api/solution/upload')
async def upload_solution(files: List[UploadFile] = File(...)):
    from db.database import upload_solution
    return upload_solution(files)

@app.post('/api/solution/create')
def create_solution(solutionData: SolutionData):
    from db.database import create_solution
    return create_solution(solutionData.Sname, solutionData.Type, solutionData.QID)

@app.get('/api/question/{QID}')
def get_question(QID: str):
    from db.database import get_question
    return get_question(QID)

@app.get('/api/fragment/{QID}')
def get_fragment(QID: str):
    from db.database import get_fragment_prototype
    return get_fragment_prototype(QID)

@app.get('/api/sequence/{BID}')
def get_sequence(BID: str):
    from db.database import get_sequence_prototype
    return get_sequence_prototype(BID)