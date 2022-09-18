# Criação das classes utilizando a biblioteca Pydantic no módulo BaseModel, que força o que foi definido pela anotação, e a tentativa de instanciá-la com outros tipos diferentes resultam erro.

from pydantic import BaseModel
from typing import List


# Classe representando os dados do cliente
class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    senha: str

class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float

class Endereco(BaseModel):
    id: int
    rua: str
    cep: str
    cidade: str
    estado: str

class ListaDeEnderecosDoUsuario(BaseModel):
    usuario: Usuario
    enderecos: List[Endereco] = []

class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    produtos: List[Produto] = []
    preco_total: float
    qtde_produtos: int