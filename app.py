from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect('database.db')
    return conn

# Crear la tabla si no existe (esto debería ejecutarse solo una vez)
def crear_tabla():
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

# Página principal: listar todos los items
@app.route('/')
def index():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()

    return render_template('index.html', items=items)

# Página para crear un nuevo item
@app.route('/crear', methods=['GET', 'POST'])
def crear_item():
    if request.method == 'POST':
        nombre = request.form['nombre']
        peso = request.form['peso']
        tamano = request.form['tamano']
        velocidad = request.form['velocidad']

        if not nombre:
            return "El nombre es obligatorio", 400

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (nombre, peso, tamano, velocidad) VALUES (?, ?, ?, ?)', (nombre, peso, tamano, velocidad))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('crear.html')

# Página para actualizar un item
@app.route('/actualizar/<int:item_id>', methods=['GET', 'POST'])
def actualizar_item(item_id):
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

        cursor.execute('UPDATE items SET nombre = ?, peso = ?, tamano = ?, velocidad = ? WHERE id = ?', (nombre, peso, tamano, velocidad, item_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('actualizar.html', item=item)

# Eliminar un item
@app.route('/eliminar/<int:item_id>', methods=['POST'])
def eliminar_item(item_id):
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
