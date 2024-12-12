import os
import uvicorn
import asyncio
import async_timeout

from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from chunks import Chunk

# инициализация индексной базы
# chunk = Chunk(path_to_base="Simble.txt")
chunk = Chunk(path_to_base="chunks.md")

# класс с типом данных для роли
class Message(BaseModel):
    content: str
    role: str

# класс с типами данных параметров
class Request(BaseModel):
    text: str
    messages: List[Message] = None

# создаем объект приложения
app = FastAPI()

# настройки для работы запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# функция обработки get запроса + декоратор 
@app.get("/")
def read_root():
    return {"message": "answer"}

# функция обработки post запроса + декоратор 
@app.post("/api/get_answer")
def get_answer(request: Request):
    print(request)
    answer = chunk.get_answer(query=request.text, last_messages=request.messages)
    return {"answer": answer}
