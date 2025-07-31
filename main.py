from tkinter import *
from tkinter import ttk
import dados

#Rota principal
root = Tk()
root.title("Gerenciador de estoque")
root.minsize(500, 400)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Frames principais
mainScreen = Frame(root)
addScreen = Frame(root)
queryScreen = Frame(root)
moveScreen = Frame(root)
editScreen = Frame(root)

#Configuraão das telas principais na rota
for tela in (mainScreen, addScreen, queryScreen, moveScreen, editScreen):
    tela.grid(row=0, column=0, sticky="nsew")
    tela.grid_rowconfigure(0, weight=1)
    tela.grid_columnconfigure(0, weight=1)

#Configuração de estilo
s = ttk.Style()
s.configure("red.TButton", background="#E53935",
                            foreground="#FFFFFF")
s.configure("yellow.TButton", background="#FFC107")
s.configure("green.TButton", background="#43A047")
s.configure("blue.TButton", background="#90CAF9")
s.configure("TLabel", font=("Arial", 11))

#Tela de cadastro
class render_addScreen():
    def __init__(self):
        #Limpa os widgets
        for widget in addScreen.winfo_children():
            widget.destroy()

        addScreen.tkraise()
        center = Frame(addScreen)
        center.grid(column=0, row=0)
        ttk.Label(center, text="Cadastrar Produto", font=("Arial", 12)).grid(column=0, row=0)
        ttk.Button(center, text="Voltar", style="blue.TButton",command=mainScreen.tkraise).grid(column=1, row=0)
        ttk.Label(center, text="Código").grid(column=0, row=1)
        ttk.Label(center, text="Nome").grid(column=0, row=2)
        ttk.Label(center, text="Quantidade").grid(column=0, row=3)
        ttk.Label(center, text="Preço").grid(column=0, row=4)

        self.codigo = StringVar()
        self.nome = StringVar()
        self.quant = StringVar(value=1)
        self.preco = StringVar()

        self.codigo_entry = ttk.Entry(center, textvariable=self.codigo)
        self.codigo_entry.grid(column=1, row=1)
        self.nome_entry = ttk.Entry(center, textvariable=self.nome)
        self.nome_entry.grid(column=1, row=2)
        self.quant_entry = ttk.Spinbox(center, from_=0, to=99999, textvariable=self.quant)
        self.quant_entry.grid(column=1, row=3)
        self.preco_entry = ttk.Entry(center, textvariable=self.preco)
        self.preco_entry.grid(column=1, row=4)

        ttk.Button(center, text="Salvar", style="green.TButton",command=self.cadastrar_produto).grid(column=0, row=5)
        ttk.Button(center, text="Limpar", command=self.limpar).grid(column=1, row=5)

        self.message = StringVar(value="")
        ttk.Label(center, textvariable=self.message).grid(column=0, row=6)

        for widget in center.winfo_children():
            widget.grid(pady=5, padx=5)
    
    def cadastrar_produto(self):
        #Tenta pegar os dados do form
        try:
            codigoValor = self.codigo.get()
            nomeValor = self.nome.get()
            quantValor = int(self.quant.get())
            precoValor = float(self.preco.get())
        except:
            self.message.set("Valores inválidos")
            return

        self.message.set("")

        #Verifica se os dados vem vazios
        if(codigoValor == "" or nomeValor == "" or quantValor == "" or precoValor == ""): 
            self.message.set("Valores inválidos")
            return

        #Tenta cadastrar o produto
        if(dados.cadastrar_produto(codigoValor, nomeValor, quantValor, precoValor)):
            self.message.set("Cadastrado com sucesso")
            self.limpar()
        else:
            self.message.set("Não foi possível cadastrar, tente mais tarde")
    
    def limpar(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.quant_entry.delete(0, END)
        self.preco_entry.delete(0, END)

#tela consulta
class render_queryScreen():

    global codigoValor
    codigoValor = ""

    def __init__(self):
        for widget in queryScreen.winfo_children():
            widget.destroy()

        center = Frame(queryScreen)
        center.grid(column=0, row=0)

        queryScreen.tkraise()

        self.code = StringVar()
        self.code.set(codigoValor)

        ttk.Label(center, text="Consulta", font=("Arial", 12)).grid(column=0, row=0)
        ttk.Button(center, text="Voltar", style="blue.TButton",command=mainScreen.tkraise).grid(column=1, row=0)
        ttk.Label(center, text="Buscar").grid(column=0, row=1)
        code_entry = ttk.Entry(center, textvariable=self.code)
        code_entry.grid(column=1, row=1)
        ttk.Button(center, text="Buscar", command=self.buscar).grid(column=3, row=1)

        self.produtos = dados.get_produtos(self.code.get())


        ttk.Label(center, text="Código").grid(column=0, row=4)
        ttk.Label(center, text="Nome").grid(column=1, row=4)
        ttk.Label(center, text="Quantidade").grid(column=2, row=4)
        ttk.Label(center, text="Preço").grid(column=3, row=4)
        for i, produto in enumerate(self.produtos):
            ttk.Label(center, text=f"{produto['codigo']}").grid(column=0, row=5+i)
            ttk.Label(center, text=f"{produto['nome']}").grid(column=1, row=5+i)
            ttk.Label(center, text=f"{produto['quantidade']}").grid(column=2, row=5+i)
            ttk.Label(center, text=f"R$ {produto['preco']:.2f}").grid(column=3, row=5+i)
            ttk.Button(center, text="Editar", style="yellow.TButton",command=lambda id=produto.doc_id: render_editScreen(id=id)).grid(column=4, row=5+i)
            ttk.Button(center, text="Deletar", style="red.TButton",command=lambda id=produto.doc_id: self.del_topScreen(id=id)).grid(column=5, row=5+i)

        self.message = StringVar()
        ttk.Label(center, textvariable=self.message).grid()
    

        for widget in center.winfo_children():
            widget.grid(pady=5, padx=5)

    #Tela para confirmar exclusão
    def del_topScreen(self, id):
        self.delTopScreen = Toplevel(root)
        ttk.Label(self.delTopScreen, text=f"Deletar {dados.get_produto_id(id)['nome']}?").grid(column=0, row=0)
        ttk.Button(self.delTopScreen, text="Cancelar", command=self.delTopScreen.destroy).grid(column=0, row=1)
        ttk.Button(self.delTopScreen, style="red.TButton",text="Confirmar", command=lambda: self.deletar_produto(id)).grid(column=2, row=1)

    #Deletar de fato
    def deletar_produto(self, id):
        if(dados.deletar_produto(id)):
            self.message.set("Produto deletado")
            self.delTopScreen.destroy()
            global codigoValor
            codigoValor = ""
            render_queryScreen()
        else:
            self.message.set("Não foi póssivel deletar, tente mais tarde")

    #Busca o produto com o código especificado
    def buscar(self):
        global codigoValor 
        codigoValor = self.code.get()
        render_queryScreen()

class render_editScreen():
    def __init__(self, id):
        self.editScreen = Toplevel(root)

        produto = dados.get_produto_id(id)

        ttk.Label(self.editScreen, text=f"Editar produto: \n {produto['nome']} | Código: {produto['codigo']}").grid(column=0, row=0)
        ttk.Button(self.editScreen, text="Fechar", style="blue.TButton",command=self.editScreen.destroy).grid(column=1, row=0)
        ttk.Label(self.editScreen, text="").grid(column=0, row=1)
        ttk.Label(self.editScreen, text=f"Nome").grid(column=0, row=2)
        ttk.Label(self.editScreen, text=f"Quantidade").grid(column=0, row=3)
        ttk.Label(self.editScreen, text=f"Preço").grid(column=0, row=4)

        self.nome = StringVar(value=produto["nome"])
        self.quant = StringVar(value=produto['quantidade'])
        self.preco = StringVar(value=f"{produto['preco']:.2f}")

        self.nome_entry = ttk.Entry(self.editScreen, textvariable=self.nome)
        self.nome_entry.grid(column=1, row=2)
        self.quant_entry = ttk.Spinbox(self.editScreen, from_=0, to=99999, textvariable=self.quant)
        self.quant_entry.grid(column=1, row=3)
        self.preco_entry = ttk.Entry(self.editScreen, textvariable=self.preco)
        self.preco_entry.grid(column=1, row=4)

        ttk.Button(self.editScreen, text="Alterar", style="green.TButton",command=lambda: self.alterar_produto(id=id)).grid(column=0, row=5)
        #ttk.Button(self.editScreen, text="Limpar").grid(column=1, row=5)

        self.message = StringVar()
        ttk.Label(self.editScreen, textvariable=self.message).grid(column=0, row=6)

        for widget in editScreen.winfo_children():
            widget.grid(pady=5, padx=5)

    def alterar_produto(self, id):
        self.message.set("")
        try:
            nomeValor = self.nome.get()
            quantValor = int(self.quant.get())
            precoValor = float(self.preco.get())
        except:
            self.message.set("Dados inválidos")

        if(nomeValor == "" or quantValor == "" or precoValor == ""):
            self.message.set("Dados inválidos")
            return
        
        if(dados.editar_produto(id, nomeValor, quantValor, precoValor)):
            self.editScreen.destroy()
            render_queryScreen()
        else:
            self.message.set("Não foi possível salvar as mudanças, tente mais tarde")

#Tela de movimentação de estoque
class render_moveScreen():

    #Lista de compras fica disponivel para das as funções
    global listaCompras
    listaCompras = []

    def __init__(self):
        #limpa o frame
        for widget in moveScreen.winfo_children():
            widget.destroy()

        center = Frame(moveScreen)
        center.grid(column=0, row=0)

        moveScreen.tkraise()

        ttk.Label(center, text="Vendas", font=("Arial", 12)).grid(column=0, row=0)
        ttk.Button(center, text="Voltar", style="blue.TButton",command=mainScreen.tkraise).grid(column=1, row=0)

        self.codigo = StringVar()
        self.quant = StringVar()

        ttk.Label(center, text="Código:").grid(column=0, row=1)
        codigo_entry = ttk.Entry(center, textvariable=self.codigo)
        codigo_entry.grid(column=1, row=1)

        ttk.Label(center, text="Quantidade").grid(column=0, row=2)
        quant_entry = ttk.Spinbox(center, textvariable=self.quant, from_=1, to=9999)
        quant_entry.grid(column=1, row=2)

        self.message = StringVar()
        ttk.Label(center, textvariable=self.message).grid(column=0, row=5)

        ttk.Button(center, text="Adicionar", style="green.TButton",command=self.addProduto).grid(column=0, row=6)
        ttk.Button(center, text="Remover", style="red.TButton",command=lambda: self.addProduto(remover=True)).grid(column=1, row=6)

        global listaCompras
        ttk.Label(center, text="Quantidade").grid(column=0, row=7)
        ttk.Label(center, text="Nome").grid(column=1, row=7)
        ttk.Label(center, text="Preço uni").grid(column=2, row=7)
        ttk.Label(center, text="Preço total").grid(column=3, row=7)

        self.preco_total = 0
        #mostrar produtos
        for i,produto in enumerate(listaCompras):
            ttk.Label(center, text=f"{produto['quantComprar']}").grid(column=0, row=8+i)
            ttk.Label(center, text=f"{produto['nome']}").grid(column=1, row=8+i)
            ttk.Label(center, text=f"{produto['preco']:.2f}").grid(column=2, row=8+i)
            ttk.Label(center, text=f"{produto['precoTotal']}").grid(column=3, row=8+i)
            self.preco_total += produto['precoTotal']

        ttk.Button(center, text="Limpar", style="red.TButton",command=self.limpar).grid(column=0)
        ttk.Button(center, style="green.TButton", text="Comprar", command=self.comprar).grid(column=0)
        ttk.Label(center, text=f"R$ {self.preco_total:.2f}").grid(column=3)

        for widget in center.winfo_children():
            widget.grid(pady=5, padx=5)

    def addProduto(self, remover = False):
        global listaCompras

        #tenta pegar os dados do form
        try:
            codigoValor = self.codigo.get()
            quantValor = -1*abs(int(self.quant.get())) if remover else abs(int(self.quant.get()))
        except:
            self.message.set("Valores inválidos")

        if(codigoValor == "" or quantValor == ""):
            self.message.set("Valores inválidos")
            return

        #Tenta pegar o produto no json
        try:
            produto = dados.get_produtos(codigoValor)
            produto = produto[0]
        except:
            self.message.set("Produto não encontrado")
            return

        #Verificar se o produto já está na lista de compra para adicionar ou remover
        for produtoCompra in listaCompras:
            if(produtoCompra['codigo'] == codigoValor):
                if(produtoCompra['quantComprar'] + quantValor > produto["quantidade"]):
                    self.message.set("Estoque insuficiente")
                    return
                elif(produtoCompra["quantComprar"] and produtoCompra['quantComprar'] - abs(quantValor) < 0):
                    produtoCompra['precoTotal'] = 0
                    produtoCompra['quantComprar'] = 0
                    render_moveScreen()
                    return
                else:
                    produtoCompra['precoTotal'] += quantValor * produtoCompra["preco"]
                    produtoCompra['quantComprar'] += quantValor
                    render_moveScreen()
                    return
        #Adiciona o produto na lista, quando não exista
        if(produto['quantidade'] < quantValor):
            self.message.set("Estoque insuficiente")
            return
        elif(remover):
            self.message.set("Produto não encontrado na lista de compra")
            return
        else:
            produto['precoTotal'] = produto['preco'] * quantValor
            produto['quantComprar'] = quantValor
            

        
        listaCompras.append(produto)
        render_moveScreen()

    def comprar(self):
        global listaCompras

        for produtoComprar in listaCompras:
            produto = dados.get_produto_id(produtoComprar.doc_id)
            novaQuantidade = produto["quantidade"] - produtoComprar["quantComprar"]
            dados.editar_produto(produtoComprar.doc_id, nova_quantidade=novaQuantidade)
        
        listaCompras = []
        self.message.set("Compra finalizada")
        render_moveScreen()
        return
    def limpar(self):
        global listaCompras

        listaCompras = []

        render_moveScreen()
         
#tela principal
class render_mainScreen:
    def __init__(self):
        center = Frame(mainScreen)
        center.grid(column=0, row=0)

        mainScreen.tkraise()
        buttons = [
            {"nome": "Cadastrar Produto", "funcao": render_addScreen},
            {"nome": "Consultar Estoque", "funcao": render_queryScreen},
            {"nome": "Vender", "funcao": render_moveScreen},
            {"nome": "Sair", "funcao": root.destroy}
        ]

        ttk.Label(center, text="Estoque", font=("Arial", 25)).grid(column=0, row=0)

        for i, button in enumerate(buttons):
            style = "red.TButton" if button["nome"] == "Sair" else "blue.TButton"
            ttk.Button(center, text=button["nome"], style=style,width="20",command=button["funcao"]).grid(column=0, row=i+1, pady=5)
    

render_mainScreen()
root.mainloop()
