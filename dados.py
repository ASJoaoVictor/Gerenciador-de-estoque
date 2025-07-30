
from tinydb import TinyDB, Query
import os

dbpath = caminho = os.path.join(os.path.dirname(__file__), 'dados.json')
db = TinyDB(dbpath)

def cadastrar_produto(codigo:str, nome:str, quantidade:int, preco:float, ):
    if(get_produtos(codigo)):
         return False
    try:
        db.insert({
          "codigo": codigo,
          "nome": nome,
          "quantidade": quantidade,
          "preco": preco
          })
        return True
    except:
        return False
     
def deletar_produto(id: int):
     try:
          db.remove(doc_ids = [id])
          return True
     except:
          print("deu erro")
          return False

def editar_produto(id, novo_nome = None, nova_quantidade = None, novo_preco = None):
     if not db.contains(doc_id=id):
          print("Produto não encontrado.")
          return False
     
     produto = get_produto_id(id)

     db.update({
          "nome": produto["nome"] if novo_nome == None else novo_nome,
          "quantidade": produto["quantidade"] if nova_quantidade == None else nova_quantidade,
          "preco": produto["preco"] if novo_preco == None else novo_preco
          }, doc_ids= [id])
     return True


def get_produto_id(id):
     produto = db.get(doc_id=id)
     return produto

def get_produtos(codigo = None):
     if(codigo == None or codigo == ""):
          return db.all()
     else:
          PRODUCT = Query()
          return db.search(PRODUCT.codigo == codigo)

