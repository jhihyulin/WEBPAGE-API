import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Header
import firebase_admin
from firebase_admin import credentials
from firebase_admin import app_check
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import datetime
import os
import dotenv
import json
from fastapi.responses import JSONResponse

from lib.TWUniversityResultQuery import search_with_test_number

dotenv.load_dotenv()

telegramBotToken = os.getenv('TGBOTTOKEN')
telegramBotAPI = "https://api.telegram.org/bot" + telegramBotToken + "/"
chatID = os.getenv('TGBOTCHATID')
appCheckIss = os.getenv('APPCHECKISS')
ServiceAccount = json.decoder.JSONDecoder().decode(os.getenv('SERVICEACCOUNT'))

class Contact(BaseModel):
    message: str
    email: str
    signature: str
    documentID: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

cred = credentials.Certificate(ServiceAccount)
firebase_admin.initialize_app(cred)

def checkTokenEffectiveness(token):
    if datetime.datetime.now().timestamp() < token['exp']:
        return True
    else:
        return False

def check(X_Firebase_AppCheck):
    if X_Firebase_AppCheck:
        token = app_check.verify_token(X_Firebase_AppCheck)
        if token:
            if checkTokenEffectiveness(token):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def notify_telegam(message):
    requests.get(telegramBotAPI + "sendMessage?chat_id=" + chatID + "&text=" + message)
    return True

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.post('/contact')
def read_contact(data: Contact, X_Firebase_AppCheck: str = Header(None)):
    if check(X_Firebase_AppCheck):
        if notify_telegam('🔔New Message\n\n💬' + data.message + '\n\n📧' + data.email + '\n\n🖋️' + data.signature + '\n\n📄' + data.documentID):
            return {'success': 'success'}
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.get('/TWUniversityResultQuery')
def read_TWUniversityResultQuery(id: str, X_Firebase_AppCheck: str = Header(None)):
    if check(X_Firebase_AppCheck):
        return JSONResponse(content=search_with_test_number(id))
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")
# def read_TWUniversityResultQuery(id: str):
#     return JSONResponse(content=search_with_test_number(id))