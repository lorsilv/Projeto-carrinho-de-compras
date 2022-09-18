from typing import List

class Busca():

    def __init__(self):
        self.db_usuarios = []
        self.db_produtos = []
        self.db_enderecos = []
        self.db_carrinhos = []

    # USUÁRIO
    def user_by_id(self, id_usuario: int): #retornar_usuario_pelo_id
        for usuario in self.db_usuarios:
            if usuario.id == id_usuario:
                return usuario

    def user_by_name(self, nome: str): #retornar_usuarios_pelo_nome
        usuarios = []
        for usuario in self.db_usuarios:
            if usuario.nome.split()[0] == nome:
                usuarios.append(usuario)
                # doc de primeira entrega fala em busca pelo primeiro nome
        return usuarios

    def password_verify(self, senha: str) -> bool: # senha_valida
        return len(senha) >= 3

    def email_verify(self, email: str) -> bool: # email_valido
        return "@" in email

    def email_verify2(self, dominio: str): #retornar_emails_mesmo_dominio
        emails = []
        for usuario in self.db_usuarios:
            if dominio == usuario.email.split("@")[1]:
                emails.append({"e-mail": usuario.email})
        return emails

    def new_user_verify(self, id: int, email: str, senha: str) -> bool:#usuario_novo_valido
        return self.email_valido(email) and self.senha_valida(senha) and not self.retornar_usuario_pelo_id(id)

    # PRODUTO
    def product_by_id (self, id: int): #retornar_produto_pelo_id
        for produto in self.db_produtos:
            if produto.id == id:
                return produto

    # CARRINHO
    def read_cart (self, id_usuario: int): #retornar_carrinho
        for carrinho in self.db_carrinhos:
            if carrinho.id_usuario == id_usuario:
                return carrinho

    def delete_cart_product(self, id_produto: int): # excluir_produto_carrinho
        for registros in self.db_carrinhos:
            for produto in registros.produtos:
                if produto.id == id_produto:
                    registros.produtos.remove(produto)

    # ENDEREÇO
    def read_user_adress (self, id_usuario: int): #retornar_enderecos_usuario
        for registro in self.db_enderecos:
            if registro.usuario.id == id_usuario:
                return registro