from genericpath import exists
from flask import Flask, request, jsonify
from utils.conect import db_connection


app = Flask(__name__)

# METODO GET
@app.route("/livros", methods=["GET"])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM livros")
        livros = [
            dict(
                id=row[0], 
                autor=row[1], 
                lingua=row[2], 
                titulo=row[3]
                )
            for row in cursor.fetchall()
        ]
        if livros is not None:
            return jsonify(livros)

# METODOS GET BY ID
@app.route("/livros/<int:id>", methods=["GET"])
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

# METODO POST
@app.route("/incluir-livros", methods=["POST"])
def create_book():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        novo_autor = request.form["autor"]
        nova_lingua = request.form["lingua"]
        novo_titulo = request.form["titulo"]
        sql = """INSERT INTO livros (autor, lingua, titulo)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (novo_autor, nova_lingua, novo_titulo))
        conn.commit()
        return "Livro adicionado com sucesso.", 201

# METODO PUT        
@app.route("/livros/<int:id>", methods=["PUT"])
def update_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == "PUT":
        autor = request.form["autor"]
        lingua = request.form["lingua"]
        titulo = request.form["titulo"]
        sql = """UPDATE livros SET autor=?, lingua=?, titulo=? WHERE id=?"""
        cursor.execute(sql, (autor, lingua, titulo, id))
        conn.commit()
        return "Livro atualizado com sucesso.", 200
        
# METODO DELETE BY ID
@app.route("/livros/<int:id>", methods=["DELETE"])
def delete_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == "DELETE":
        cursor.execute("DELETE FROM livros WHERE id=?", (id,))
        conn.commit()
        return "Livro excluído com sucesso.", 200
    

if __name__ == "__main__":
    app.run(debug=True)