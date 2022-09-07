from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)


#Base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT '] = 3306
app.config['MYSQL_USER'] = 'root'	
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contactosdb'

mysql = MySQL(app)


# Llave secreta
app.secret_key = 'my_secret_key'


# Ruta principal
@app.route('/')
def index():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()

    return render_template('index.html', contacts = data)


# Ruta para agregar contacto
@app.route('/add_contact', methods=['POST'])
def add_contact():

    if request.method == 'POST':

        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()

        flash('Successfully added contact!')

        return redirect(url_for('index'))


# Ruta para editar contacto 
@app.route('/edit_contact/<id>')
def edit_contact(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cursor.fetchall()

    return render_template('edit-contact.html', contact = data[0])


# Ruta para actualizar el contacto
@app.route('/updated_contact/<id>', methods=['POST'])
def updated_contact(id):

    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s    
        """, (fullname, phone, email, id))

        mysql.connection.commit()

        flash('Successfully updated contact!')

        return redirect(url_for('index'))


# Ruta para eliminar contacto
@app.route('/delete_contact/<id>')
def delete_contact(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = %s', [id])
    mysql.connection.commit()

    flash('Successfully removed contact!')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)


