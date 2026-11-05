# TechStock Manager

Projeto desenvolvido para a TechStore Informática & Serviços Corporativos, com o objetivo de organizar o estoque de equipamentos, periféricos e licenças de software.

O sistema permite consultar os produtos, cadastrar novos itens e registrar entradas e saídas de estoque.

## Funcionalidades

- Dashboard com produtos, categorias e fornecedores.
- Cadastro de produtos com seleção de categoria e fornecedor.
- Controle de entradas e saídas com histórico de movimentações.
- Bloqueio de saídas com quantidade superior ao estoque disponível.
- Alerta quando o saldo está igual ou abaixo do estoque mínimo.
- Validação de SKU duplicado, preço inválido e estoque negativo.
- Exclusão de produtos, categorias e fornecedores com proteção dos vínculos existentes.

## Tecnologias utilizadas

- Python 3.14.7
- Flask 3.1.3
- pyodbc 5.3.0
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server
- HTML e CSS

## Pré-requisitos

Para executar o projeto no Windows, é necessário ter:

- Python com pip disponível no terminal.
- SQL Server instalado e em execução.
- SQL Server Management Studio (SSMS).
- ODBC Driver 17 for SQL Server.

## Preparação do ambiente

Baixe e extraia o projeto ou clone o repositório pelo GitHub.

Abra o terminal na pasta que contém o arquivo `app.py` e crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente conforme o terminal utilizado.

No Prompt de Comando (CMD):

```bat
.venv\Scripts\activate.bat
```

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação, utilize o Prompt de Comando.

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Criação do banco de dados

1. Abra o SQL Server Management Studio.
2. Conecte-se à instância do SQL Server que será utilizada.
3. Abra o arquivo `database.sql`.
4. Execute o script completo pressionando F5.

O script cria o banco `TechStock` e as tabelas:

- Categorias
- Fornecedores
- Produtos
- Movimentacoes

Também adiciona os dados iniciais de teste: 4 categorias, 3 fornecedores e 6 produtos, incluindo hardware e licenças de software.

Execute esse script apenas na criação inicial. Ele não foi preparado para ser repetido em um banco já existente.

## Configuração da conexão

No arquivo `app.py`, a função `conectar()` utiliza esta configuração:

```python
def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=TechStock;"
        "Trusted_Connection=yes;"
    )
```

O servidor configurado é `localhost\SQLEXPRESS`. Caso sua instância tenha outro nome, altere o valor de `SERVER` para o mesmo nome utilizado na conexão do SSMS.

A opção `Trusted_Connection=yes` utiliza a autenticação do Windows. O usuário que executa a aplicação precisa ter permissão de acesso ao banco `TechStock`.

## Execução da aplicação

Com o banco criado, a conexão configurada e as dependências instaladas, execute:

```bash
python app.py
```

Abra no navegador:

http://127.0.0.1:5000

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

O comando inicia o Flask em modo de desenvolvimento, com depuração ativada.

## Como utilizar

1. Acesse o dashboard para consultar o estoque.
2. Utilize o formulário de cadastro para adicionar produtos.
3. Na área de movimentação, selecione o produto, o tipo de operação e a quantidade.
4. Registre uma entrada para aumentar o saldo ou uma saída para reduzir.
5. Acompanhe os alertas de reposição no dashboard.

Produtos com movimentações registradas não podem ser excluídos. Categorias e fornecedores com produtos vinculados também têm a exclusão bloqueada.

## Estrutura do projeto

```text
techstock/
├── app.py
├── database.sql
├── README.md
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── cadastros.html
    ├── dashboard.html
    ├── movimentacao.html
    └── produto_form.html
```