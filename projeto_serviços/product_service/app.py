from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

import uvicorn

# Definição do arquivo de banco de dados SQLite
sqlite3_db = 'product_db.sqlite'

# Conexão com o banco de dados
conn = sqlite3.connect(sqlite3_db, check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela de produtos se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        price REAL
    )
''')
conn.commit()



# Classe modelo para produto
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

# Funções de CRUD
def get_product_by_id(product_id: int):
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    if product:
        return Product(id=product[0], name=product[1], description=product[2], price=product[3])
    else:
        return None

def get_products():
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return [Product(id=product[0], name=product[1], description=product[2], price=product[3]) for product in products]

# Configuração do FastAPI
app = FastAPI()

# Rota para verificar se o serviço está rodando
@app.get('/')
def hello_world():
    return {"message": "Serviço de Produtos"}

# Rota para obter todos os produtos
@app.get('/products', response_model=List[Product])
def read_products():
    return get_products()

# Rota para obter um produto específico por ID
@app.get('/product/{product_id}', response_model=Product)
def read_product(product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

# Rota para criar um novo produto via formulário HTML
@app.post('/create_product_rpc/')
async def create_product_rpc(name: str = Form(...), description: str = Form(...), price: float = Form(...)):
    cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', (name, description, price))
    conn.commit()
    return {"message": "Produto criado com sucesso"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
