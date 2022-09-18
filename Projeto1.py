# Importando o framework para API:
from fastapi import FastAPI
# Importando as classes com os modelos:
from classes import Usuario
from classes import Produto
from classes import Endereco
from classes import ListaDeEnderecosDoUsuario
from classes import CarrinhoDeCompras
#Importanto programa para busca de dados:
from busca_dados import Busca as bd


app = FastAPI()


OK = "OK"
FALHA = "FALHA"

#Cria usuário utilizando dados de id, email e senha. Modelo definido em "classes"

@app.post("/usuario/")
async def criar_usuário(usuario: Usuario):
    if bd.new_user_verify(usuario.id, usuario.email, usuario.senha):
        bd.db_usuarios.append(usuario)
        return OK
    return FALHA

#Retorna usuário a partir de 

@app.get("/usuario/")
async def retornar_usuario(id: int):
    usuario_encontrado = bd.user_by_id(id)
    return usuario_encontrado if usuario_encontrado else FALHA


@app.get("/usuario/nome/")
async def retornar_usuario_com_nome(nome: str):
    usuario_encontrado = bd.user_by_name(nome)
    return usuario_encontrado if usuario_encontrado else FALHA


@app.delete("/usuario/")
async def deletar_usuario(id: int):
    usuario_encontrado = bd.user_by_id(id)
    carrinho_encontrado = bd.read_cart(id)
    enderecos_encontrados = bd.read_user_adress(id)
    if usuario_encontrado:
        bd.db_usuarios.remove(usuario_encontrado)
        if carrinho_encontrado:
            bd.db_carrinhos.remove(carrinho_encontrado)
        if enderecos_encontrados:
            bd.db_enderecos.remove(enderecos_encontrados)
        return OK
    return FALHA


@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Endereco, id_usuario: int):
    usuario_cadastrado = bd.user_by_id(id_usuario)
    enderecos_encontrados = bd.read_user_adress(id_usuario)
    if usuario_cadastrado:
        if enderecos_encontrados:
            enderecos_encontrados.append(endereco)
        else:
            bd.db_enderecos.append(ListaDeEnderecosDoUsuario(
                usuario=usuario_cadastrado, enderecos=[endereco]))
        return OK
    return FALHA

@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    enderecos_encontrados = bd.read_user_adress(id_usuario)
    if enderecos_encontrados:
        return enderecos_encontrados
    return FALHA


@app.delete("/usuario/{id_usuario}/endereco/{id_endereco}")
async def deletar_endereco(id_usuario: int, id_endereco: int):
    enderecos_encontrados = bd.read_user_adress(id_usuario)
    if enderecos_encontrados:
        for endereco in enderecos_encontrados:
            if endereco.id == id_endereco:
                enderecos_encontrados.remove(endereco)
                return OK
    return FALHA


@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    emails_encontrados = bd.email_verify2(dominio)
    return emails_encontrados if emails_encontrados else FALHA


@app.post("/produto/")
async def criar_produto(produto: Produto):
    produto_encontrado = bd.product_by_id(produto.id)
    if not produto_encontrado:
        bd.db_produtos.append(produto)
        return OK
    return FALHA


@app.get("/produto/{id_produto}/")
async def consultar_produto(id_produto: int):
    produto_encontrado = bd.product_by_id(id_produto)
    if produto_encontrado:
        return produto_encontrado
    return FALHA


@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    produto_cadastrado = bd.product_by_id(id_produto)
    if produto_cadastrado:
        bd.db_produtos.remove(produto_cadastrado)
        bd.delete_cart_product(id_produto)
        return OK
    return FALHA


@app.post("/carrinho/{id_usuario}/{id_produto}")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    usuario_cadastrado = bd.user_by_id(id_usuario)
    produto_cadastrado = bd.product_by_id(id_produto)
    carrinho_cadastrado = bd.read_cart(id_usuario)

    if usuario_cadastrado and produto_cadastrado:
        if carrinho_cadastrado:
            carrinho_cadastrado.produtos.append(produto_cadastrado)
            carrinho_cadastrado.preco_total += produto_cadastrado.preco
            carrinho_cadastrado.qtde_produtos = len(
                carrinho_cadastrado.produtos)
        else:
            carrinho = CarrinhoDeCompras(id_usuario=id_usuario, produtos=[produto_cadastrado],
                                         preco_total=produto_cadastrado.preco, qtde_produtos=1)
        bd.db_carrinhos.append(carrinho)
        return OK
    return FALHA


@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    carrinho_cadastrado = bd.read_cart(id_usuario)
    return carrinho_cadastrado if carrinho_cadastrado else FALHA


@app.get("/carrinho/total/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
    carrinho_cadastrado = bd.read_cart(id_usuario)
    soma_precos = 0
    if carrinho_cadastrado:
        for produtos in carrinho_cadastrado.produtos:
            soma_precos += produtos.preco
        return {"produtos": carrinho_cadastrado.qtde_produtos, "total (R$)": soma_precos}
    else:
        return FALHA


@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    carrinho_cadastrado = bd.read_cart(id_usuario)
    if carrinho_cadastrado:
        bd.db_carrinhos.remove(carrinho_cadastrado)
        return OK
    return FALHA


@app.get("/")
async def bem_vinda():
    site = "Seja bem-vinda!"
    return site.replace('\n', '')