"""
API REST
"""

import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def conectar_db():
    """Conexión a la base de datos SQLite"""
    conn = sqlite3.connect('database.db')
    return conn

def crear_tabla():
    """Crear la tabla si no existe (esto debería ejecutarse solo una vez)"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            peso TEXT,
            tamano TEXT,
            velocidad TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal: listar todos los items"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()

    return render_template('index.html', items=items)

@app.route('/crear', methods=['GET', 'POST'])
def crear_item():
    """Página para crear un nuevo item"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        peso = request.form['peso']
        tamano = request.form['tamano']
        velocidad = request.form['velocidad']

        if not nombre:
            return "El nombre es obligatorio", 400

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO items (nombre, peso, tamano, velocidad) VALUES (?, ?, ?, ?)',
            (nombre, peso, tamano, velocidad))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('crear.html')

@app.route('/actualizar/<int:item_id>', methods=['GET', 'POST'])
def actualizar_item(item_id):
    """Página para actualizar un item"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if item is None:
        return "Item no encontrado", 404

    if request.method == 'POST':
        nombre = request.form['nombre']
        peso = request.form['peso']
        tamano = request.form['tamano']
        velocidad = request.form['velocidad']

        cursor.execute(
            'UPDATE items SET nombre = ?, peso = ?, tamano = ?, velocidad = ? WHERE id = ?',
            (nombre, peso, tamano, velocidad, item_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('actualizar.html', item=item)

@app.route('/eliminar/<int:item_id>', methods=['POST'])
def eliminar_item(item_id):
    """Eliminar un item"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Ejecuta la aplicación Flask
if __name__ == '__main__':
    crear_tabla()
    app.run(debug=True)
