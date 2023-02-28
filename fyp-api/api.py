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
    UID: str

class UpdateQuestionSolutionSeqData(BaseModel):
    SolutionSeq: str
class UpdateQuestionTypeData(BaseModel):
    Type: str
class SolutionData(BaseModel):
    Sname: str
    Type: str
    QID: str

class DistractorData(BaseModel):
    Code: str
    Reason: str
    FID: str

class FeedbackData(BaseModel):
    Content: str
    DID: str

class DifficultyLevelData(BaseModel):
    Level: str
    BlockSeq: str
    SID: str

class BlockData(BaseModel):
    Type: str
    FragmentSeq: str
    DLID: str

class UpdateDifficultyLevelData(BaseModel):
    Level: str
    BlockSeq: str
    SID: str

class UpdateSolutionData(BaseModel):
    Type: str

class FragmentTypeData(BaseModel):
    Type: str

class UserData(BaseModel):
    Email: str
    Password: str
    Uname: str
    UType: str
    CID: str

class CreateRecordData(BaseModel):
    UID: str
    QID: str
    Score: str

class UpdateRecordData(BaseModel):
    Score: str

class CreateEasierVersionData(BaseModel):
    QID: str
    UID: str

@app.get("/api/")
async def root():
    return {"message": "Hello World"}

@app.post('/api/login_check/')
async def login(loginData: LoginData):
    from db.database import login_check
    return login_check(loginData.email, loginData.password)

# @app.post('/api/register/')
# def register(registerData: RegisterData):
#     from db.database import create_account
#     return create_account(registerData.email.split('@')[0], registerData.email, registerData.password, 'user')

@app.post('/api/question/create')
def create_question(questionData: QuestionData):
    from db.database import create_question_prototype
    return create_question_prototype(questionData.Qname, questionData.Scope, questionData.Description, questionData.Type, questionData.UID)

@app.post('/api/question_solution_seq/update/{QID}')
def update_question_solution_seq(QID: str, updateQuestionSolutionSeqData: UpdateQuestionSolutionSeqData):
    from db.database import update_question_solution_seq
    return update_question_solution_seq(QID, updateQuestionSolutionSeqData.SolutionSeq)

@app.post('/api/question_type/update/{QID}')
def update_question_type(QID: str, updateQuestionTypeData: UpdateQuestionTypeData):
    from db.database import update_question_type
    return update_question_type(QID, updateQuestionTypeData.Type)

@app.post('/api/solution/upload')
async def upload_solution(files: List[UploadFile] = File(...)):
    from db.database import upload_solution
    return upload_solution(files)

@app.post('/api/solution/create')
def create_solution(solutionData: SolutionData):
    from db.database import create_solution
    return create_solution(solutionData.Sname, solutionData.Type, solutionData.QID)

@app.get('/api/question/getAll')
def get_all_question():
    from db.database import get_all_question
    return get_all_question()

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

@app.post('/api/distractor/create')
def create_distractor(distractorData: DistractorData):
    from db.database import create_distractor
    return create_distractor(distractorData.Code, distractorData.Reason, distractorData.FID)

@app.post('/api/difficulty_level/create')
def create_difficulty_level(difficultyLevelData: DifficultyLevelData):
    from db.database import create_difficulty_level
    return create_difficulty_level(difficultyLevelData.Level, difficultyLevelData.BlockSeq, difficultyLevelData.SID)

@app.post('/api/block/create')
def create_block(blockData: BlockData):
    from db.database import create_block
    return create_block(blockData.Type, blockData.FragmentSeq, blockData.DLID)

@app.post('/api/difficulty_level/update/{DLID}')
def update_difficulty_level(DLID: str, updateDifficultyLevelData: UpdateDifficultyLevelData):
    from db.database import update_difficulty_level
    return update_difficulty_level(DLID, updateDifficultyLevelData.Level, updateDifficultyLevelData.BlockSeq, updateDifficultyLevelData.SID)

@app.post('/api/solution/update/{SID}')
def update_solution(SID: str, updateSolutionData: UpdateSolutionData):
    from db.database import update_solution_prototype
    return update_solution_prototype(SID, updateSolutionData.Type)

@app.get('/api/distractor/{FID}')
def get_distractor(FID: str):
    from db.database import get_distractor_by_fid
    return get_distractor_by_fid(FID)

@app.post('/api/fragment_type/update/{FID}')
def update_fragment_type(FID: str, fragmentTypeData: FragmentTypeData):
    from db.database import update_fragment_type
    return update_fragment_type(FID, fragmentTypeData.Type)

@app.get('/api/fragment_fid/{FID}')
def get_fragment_id(FID: str):
    from db.database import get_fragment
    return get_fragment(FID)

@app.get('/api/block/{QID}')
def get_block(QID: str):
    from db.database import get_block_multiple_steps
    return get_block_multiple_steps(QID)

@app.get('/api/solution_name/{BID}')
def get_solution_name(BID: str):
    from db.database import get_solution_name
    return get_solution_name(BID)

@app.post('/api/easier_version/create')
def create_easier_version(createEasierVersionData: CreateEasierVersionData):
    from db.database import create_easier_version_pointer
    return create_easier_version_pointer(createEasierVersionData.QID, createEasierVersionData.UID)

@app.get('/api/easier_version/check/{QID}')
def check_easier_version(QID: str):
    from db.database import check_easier_version
    return check_easier_version(QID)

@app.get('/api/class/getAll')
def get_all_class():
    from db.database import get_all_class
    return get_all_class()

@app.post('/api/user/create')
def create_user(userData: UserData):
    from db.database import create_user
    return create_user(userData.Uname, userData.Password, userData.Email, userData.UType, userData.CID)

@app.post('/api/record/create')
def create_record(createRecordData: CreateRecordData):
    from db.database import create_record
    return create_record(createRecordData.UID, createRecordData.QID)
@app.post('/api/record/update/{UID}/{QID}')
def update_record(UID: str, QID: str, updateRecordData: UpdateRecordData):
    from db.database import update_record
    return update_record(UID, QID, updateRecordData.Score)
@app.get('/api/record/getAll/{UID}')
def get_all_record(UID: str):
    from db.database import get_all_record
    return get_all_record(UID)
@app.get('/api/record/{UID}/{QID}')
def get_record(UID: str, QID: str):
    from db.database import get_record
    return get_record(UID, QID)
