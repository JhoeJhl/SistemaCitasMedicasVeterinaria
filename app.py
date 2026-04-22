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

#rutas
@app.route('/') #muestra todas las citas
def agenda():
    pass

@app.route('/agendar') #redirige al formulario para registrar una cita
def agendar():
    render_template('create.html')

@app.route('/guardarcita', methods=['POST']) #guarda en la base de datos el registro de create.html
def method_name():
    pass

@app.route('/modificar/<int:id>', methods=['POST']) # redirige al edit.html para editar un registro en especifico
def modificar(id):
    pass

@app.route('/cancelar/<int:id>') #elimina un registro en especifico
def method_name():
    pass

if __name__=='__main__':
    app.run(debug=True)