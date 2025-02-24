from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import sqlite3
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Rota principal para exibir o formulário
@app.get("/aichat")
async def read_root(request: Request):
    return templates.TemplateResponse("aichat.html", {"request": request, "resposta": None})

# Rota para processar o formulário e obter resposta do Grok
@app.post("/enviar")
async def enviar_mensagem(request: Request, mensagem: str = Form(...)):
    # Invoca a chain com a mensagem do usuário
    resposta = chain.invoke({"mensagem": mensagem})
    # Retorna o template com a resposta
    return templates.TemplateResponse("aichat.html", {"request": request, "resposta": resposta, "mensagem": mensagem})


# Configura o modelo Grok via LangChain
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="deepseek-r1-distill-llama-70b", groq_api_key=groq_api_key)

# Define o template de prompt
system_template = "Você é um assistente útil. Responda à seguinte mensagem: {mensagem}"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{mensagem}")
])

# Configura o parser para extrair a resposta como string
parser = StrOutputParser()

# Cria a chain (cadeia) do LangChain
chain = prompt_template | llm | parser



class User(BaseModel):
    name: str
    username: str
    email: str

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 username TEXT NOT NULL UNIQUE,
                 email TEXT NOT NULL UNIQUE
                 )''')
    conn.commit()
    conn.close()

@app.get("/register", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...)
):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, username, email) VALUES (?, ?, ?)",
            (name, username, email)
        )
        conn.commit()
        conn.close()
        return RedirectResponse(url="/", status_code=303)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists!")

@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Adiciona isso para retornar dicionários
    c = conn.cursor()
    c.execute("SELECT id, name, username, email FROM users")
    users = c.fetchall()
    conn.close()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/chat", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


