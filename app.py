from flask import Flask, request, render_template, url_for, redirect
import sqlite3


app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('citas.db')
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes(
            id INTEGER PRIMARY KEY, 
            mascota TEXT NOT NULL,
            propietario TEXT NOT NULL, 
            especie TEXT NOT NULL, 
            fecha DATE NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

#Inicializacion de la base de datos
init_db()

#RUTAS
@app.route('/') #muestra todas las citas
def agenda():

    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')

    consulta = cursor.fetchall()

    return render_template('index.html', consulta=consulta)

@app.route('/agendar') #redirige al formulario para registrar una cita
def agendar():
    return render_template('create.html')

#guarda en la base de datos el registro de create.html
@app.route('/guardarcita', methods=['POST']) 
def guardarcita():
   mascota = request.form['mascota']
   propietario = request.form['propietario']
   especie = request.form['especie']
   fecha = request.form['fecha']

   conn = sqlite3.connect('citas.db')
   cursor = conn.cursor()
   cursor.execute('INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?,?,?,?)', (mascota, propietario, especie, fecha))
   conn.commit()
   conn.close()

   return redirect("/")

#redirige al edit.html para editar un registro en especifico
@app.route('/modificar/<int:id>', methods=['POST']) 
def modificarcita(id):
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    persona = cursor.fetchone()

    return render_template('edit.html', persona=persona)

#procesa la actualizacion del registro
@app.route('/update_cita', methods=['POST'])
def update_cita():
    id = request.form['id']
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']

    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE pacientes SET mascota = ?, propietario = ?, especie = ?, fecha = ? WHERE id = ?', (mascota, propietario, especie, fecha, id))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route('/cancelar/<int:id>') #elimina un registro en especifico
def cancelarcita(id):
    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pacientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__=='__main__':
    app.run(debug=True)