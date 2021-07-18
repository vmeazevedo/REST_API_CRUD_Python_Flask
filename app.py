from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

# CONEXÃO COM A BASE DE DADOS
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("livros.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

# METODOS GET E POST
@app.route("/livros", methods=["GET", "POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM livros")
        livros = [
            dict(id=row[0], autor=row[1], lingua=row[2], titulo=row[3])
            for row in cursor.fetchall()
        ]
        if livros is not None:
            return jsonify(livros)

    if request.method == "POST":
        novo_autor = request.form["autor"]
        nova_lingua = request.form["lingua"]
        novo_titulo = request.form["titulo"]
        sql = """INSERT INTO livros (autor, lingua, titulo)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (novo_autor, nova_lingua, novo_titulo))
        conn.commit()
        return "Livro adicionado com sucesso.".format(id), 201
        

# METODOS GET BY ID, PUT, DELETE
@app.route("/livros/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    livros = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM livros WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            livros = r
        if livros is not None:
            return jsonify(livros), 200
        else:
            return "Id não cadastrado.", 404

    if request.method == "PUT":
        sql = """UPDATE livros
                SET titulo=?,
                    autor=?,
                    lingua=?
                WHERE id=? """

        autor = request.form["autor"]
        lingua = request.form["lingua"]
        titulo = request.form["titulo"]
        atualiza_livro = {
            "id": id,
            "autor": autor,
            "lingua": lingua,
            "titulo": titulo,
        }
        conn.execute(sql, (autor, lingua, titulo, id))
        conn.commit()
        return jsonify(atualiza_livro)

    if request.method == "DELETE":
        sql = """ DELETE FROM livros WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "O livro com o id: {} foi deletado.".format(id), 200


if __name__ == "__main__":
    app.run(debug=True)