from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = "techstock"


# Conexao com o SQL Server
# Troque o SERVER pelo nome que aparece quando voce abre o SSMS
def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=TechStock;"
        "Trusted_Connection=yes;"
    )


# R1 - Dashboard com INNER JOIN
@app.route("/")
def dashboard():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.sku, p.nome, p.fabricante, c.nome AS categoria,
               f.razao_social AS fornecedor, p.preco, p.estoque,
               p.estoque_minimo, p.localizacao, p.licenciamento
        FROM Produtos p
        INNER JOIN Categorias c ON p.categoria_id = c.id
        INNER JOIN Fornecedores f ON p.fornecedor_id = f.id
        ORDER BY p.nome
    """)
    produtos = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", produtos=produtos)


# R2 - Cadastro de produto
@app.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        sku = request.form["sku"].upper()
        nome = request.form["nome"]
        fabricante = request.form["fabricante"]
        tipo = request.form["tipo"]
        especificacao = request.form["especificacao"]
        licenciamento = request.form["licenciamento"]
        preco = float(request.form["preco"])
        estoque = int(request.form["estoque"])
        estoque_minimo = int(request.form["estoque_minimo"])
        localizacao = request.form["localizacao"]
        categoria_id = request.form["categoria_id"]
        fornecedor_id = request.form["fornecedor_id"]

        # licenciamento so existe para software
        if tipo != "Software" or licenciamento == "":
            licenciamento = None

        # validacoes
        cursor.execute("SELECT id FROM Produtos WHERE sku = ?", (sku,))
        sku_existente = cursor.fetchone()

        if sku_existente is not None:
            flash("Erro: ja existe um produto com esse SKU.", "erro")
        elif preco <= 0:
            flash("Erro: o preco precisa ser maior que zero.", "erro")
        elif estoque < 0 or estoque_minimo < 0:
            flash("Erro: o estoque nao pode ser negativo.", "erro")
        else:
            cursor.execute("""
                INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao,
                    licenciamento, preco, estoque, estoque_minimo, localizacao,
                    categoria_id, fornecedor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (sku, nome, fabricante, tipo, especificacao, licenciamento,
                  preco, estoque, estoque_minimo, localizacao,
                  categoria_id, fornecedor_id))
            conn.commit()
            conn.close()
            flash("Produto cadastrado com sucesso!", "sucesso")
            return redirect(url_for("dashboard"))

    # busca categorias e fornecedores para os selects
    cursor.execute("SELECT id, nome FROM Categorias ORDER BY nome")
    categorias = cursor.fetchall()
    cursor.execute("SELECT id, razao_social FROM Fornecedores ORDER BY razao_social")
    fornecedores = cursor.fetchall()
    conn.close()
    return render_template("produto_form.html", categorias=categorias, fornecedores=fornecedores)


# R3 - Entrada e saida de estoque
@app.route("/movimentacao", methods=["GET", "POST"])
def movimentacao():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        produto_id = request.form["produto_id"]
        tipo = request.form["tipo"]
        quantidade = int(request.form["quantidade"])
        observacao = request.form["observacao"]

        cursor.execute("SELECT nome, estoque FROM Produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if quantidade <= 0:
            flash("Erro: a quantidade precisa ser maior que zero.", "erro")
        elif tipo == "Saida" and quantidade > produto.estoque:
            flash("Erro: saida bloqueada. Estoque disponivel de " + produto.nome +
                  ": " + str(produto.estoque) + " unidades.", "erro")
        else:
            if tipo == "Entrada":
                cursor.execute("UPDATE Produtos SET estoque = estoque + ? WHERE id = ?",
                               (quantidade, produto_id))
            else:
                cursor.execute("UPDATE Produtos SET estoque = estoque - ? WHERE id = ?",
                               (quantidade, produto_id))

            cursor.execute("""
                INSERT INTO Movimentacoes (tipo, quantidade, observacao, produto_id)
                VALUES (?, ?, ?, ?)
            """, (tipo, quantidade, observacao, produto_id))
            conn.commit()
            conn.close()
            flash("Movimentacao registrada com sucesso!", "sucesso")
            return redirect(url_for("dashboard"))

    cursor.execute("SELECT id, sku, nome, estoque FROM Produtos ORDER BY nome")
    produtos = cursor.fetchall()
    cursor.execute("""
        SELECT TOP 10 m.data_hora, p.sku, p.nome, m.tipo, m.quantidade, m.observacao
        FROM Movimentacoes m
        INNER JOIN Produtos p ON m.produto_id = p.id
        ORDER BY m.id DESC
    """)
    historico = cursor.fetchall()
    conn.close()
    return render_template("movimentacao.html", produtos=produtos, historico=historico)


# R4 - Exclusao de itens
@app.route("/produtos/<int:id>/excluir", methods=["POST"])
def excluir_produto(id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Produtos WHERE id = ?", (id,))
        conn.commit()
        flash("Produto excluido com sucesso.", "sucesso")
    except pyodbc.IntegrityError:
        flash("Nao e possivel excluir: este produto possui movimentacoes registradas.", "erro")
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/cadastros")
def cadastros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM Categorias ORDER BY nome")
    categorias = cursor.fetchall()
    cursor.execute("SELECT id, razao_social, cnpj FROM Fornecedores ORDER BY razao_social")
    fornecedores = cursor.fetchall()
    conn.close()
    return render_template("cadastros.html", categorias=categorias, fornecedores=fornecedores)

# Cadastro de fornecedor
@app.route("/fornecedores/novo", methods=["GET", "POST"])
def novo_fornecedor():
    if request.method == "POST":
        razao_social = request.form["razao_social"]
        cnpj = request.form["cnpj"]
        telefone = request.form["telefone"]
        email = request.form["email"]

        # deixa so os numeros do CNPJ
        cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()

        if len(cnpj) != 14 or not cnpj.isdigit():
            flash("Erro: o CNPJ precisa ter 14 numeros.", "erro")
        else:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM Fornecedores WHERE cnpj = ?", (cnpj,))
            cnpj_existente = cursor.fetchone()

            if cnpj_existente is not None:
                flash("Erro: ja existe um fornecedor com esse CNPJ.", "erro")
                conn.close()
            else:
                cursor.execute("""
                    INSERT INTO Fornecedores (razao_social, cnpj, telefone, email)
                    VALUES (?, ?, ?, ?)
                """, (razao_social, cnpj, telefone, email))
                conn.commit()
                conn.close()
                flash("Fornecedor cadastrado com sucesso!", "sucesso")
                return redirect(url_for("cadastros"))

    return render_template("fornecedor_form.html")


@app.route("/categorias/<int:id>/excluir", methods=["POST"])
def excluir_categoria(id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Categorias WHERE id = ?", (id,))
        conn.commit()
        flash("Categoria excluida com sucesso.", "sucesso")
    except pyodbc.IntegrityError:
        flash("Nao e possivel excluir: esta categoria ainda possui produtos vinculados.", "erro")
    conn.close()
    return redirect(url_for("cadastros"))


@app.route("/fornecedores/<int:id>/excluir", methods=["POST"])
def excluir_fornecedor(id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Fornecedores WHERE id = ?", (id,))
        conn.commit()
        flash("Fornecedor excluido com sucesso.", "sucesso")
    except pyodbc.IntegrityError:
        flash("Nao e possivel excluir: este fornecedor ainda possui produtos vinculados.", "erro")
    conn.close()
    return redirect(url_for("cadastros"))


if __name__ == "__main__":
    app.run(debug=True)
