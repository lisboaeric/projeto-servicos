from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

import uvicorn

# Definição do nome do arquivo de banco de dados SQLite
sqlite3_db = 'user_db.sqlite'

# Conexão com o banco de dados
conn = sqlite3.connect(sqlite3_db, check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela de usuários se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
''')
conn.commit()



# Classe modelo para usuário
class User(BaseModel):
    id: int
    username: str
    password: str

# Funções de CRUD
def get_user_by_id(user_id: int):
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user:
        return User(id=user[0], username=user[1], password=user[2])
    else:
        return None

def get_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return [User(id=user[0], username=user[1], password=user[2]) for user in users]

# Configuração do FastAPI
app = FastAPI()

# Rota para verificar se o serviço está rodando
@app.get('/')
def hello_world():
    return {"message": "Serviço de usuários"}

# Rota para obter todos os usuários
@app.get('/users', response_model=List[User])
def read_users():
    return get_users()

# Rota para obter um usuário específico por ID
@app.get('/user/{user_id}', response_model=User)
def read_user(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Rota para criar um novo usuário via formulário HTML
@app.post('/create_user_rpc/')
async def create_user_rpc(username: str = Form(...), password: str = Form(...)):
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    return {"message": "Usuário criado com sucesso"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
