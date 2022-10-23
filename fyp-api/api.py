import email
import os
import re
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
from typing import Optional

SECRET_KEY = "6a5c696a4469597fe2962bcd83e05846fe86ec5bbde835c7983955a295e092da"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080

fpath = os.path.join(os.path.dirname(__file__), 'db')
sys.path.append(fpath)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default='Bearer')

class TokenData(BaseModel):
    username: str = None

class User(BaseModel):
    email: str
    UID: str
    type: str

class LoginData(BaseModel):
    # remember: bool
    email: str
    password: str
    # remember_me: str

class ChangePasswordData(BaseModel):
    email: str
    oldPassword: str
    newPassword: str

class RegisterData(BaseModel):
    email: str
    password: str

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
