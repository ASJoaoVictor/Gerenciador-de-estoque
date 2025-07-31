# 📦 Gerenciador de Estoque

Sistema simples de controle de estoque com interface gráfica em Tkinter, desenvolvido em Python. Ele permite o cadastro, edição, exclusão e busca de produtos, além de controlar a saída de itens do estoque.

## 🛠️ Tecnologias Utilizadas

- Python
- Tkinter (interface gráfica)
- TinyDB (banco de dados leve em JSON)
- JSON (armazenamento dos dados)

## 💡 Funcionalidades

- ✅ Cadastro de produtos
- ✏️ Edição de produtos cadastrados
- ❌ Exclusão de produtos
- 🔍 Busca por código do produto
- 📤 Saída de estoque(Venda)

## 🖥️ Interface

Aplicação **desktop** com interface gráfica feita em **Tkinter**.

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/gerenciador-estoque.git
   cd gerenciador-estoque
   ```

2. Crie e ative um ambiente virtual Python (recomendado):
    - Windows
       ```bash
       python -m venv venv
       ```
      ```
      venv\Scripts\activate
      ```
    - Linux/mac
      ```bash
      python3 -m venv venv
      ```
      ```
      source venv/bin/activate
      ```
4. Instale a dependência principal:
   ```bash
   pip install tinydb
   ```
5. (Opcional) Se Tkinter não estiver instalado, instale manualmente:
     - Ubuntu/Debian:
         ```bash
         sudo apt-get install python3-tk
         ```
     - Fedora:
       ```bash
       sudo dnf install python3-tkinter
       ```
6. Execute o sistema:
     - Windows
         ```bash
         python main.py
         ```
      - Linux/mac
         ```bash
         python3 main.py
         ```
## 📂 Estrutura dos Dados
Os dados são armazenados localmente em arquivos .json por meio do TinyDB, eliminando a necessidade de um banco de dados tradicional.

## 📄 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
   
   

