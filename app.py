from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

app = Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/imagen')
def imagen():
    print('imagen')
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)


@app.route('/licores')
def licores():
    return render_template('sitio/licores.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/licores')
def admin_licores():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `productos`")
    licores=cursor.fetchall()
    conexion.commit()
    print(licores)
    return render_template("admin/licores.html", licores=licores)

@app.route('/admin/licores/guardar', methods=['POST'])
def admin_licores_guardar():
    _nombre=request.form['txtnombre']
    _descarga=request.form['txtdescarga']
    _archivo=request.files['txtimagen']

    tiempo= datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!='':
        nuevoNombre=horaActual+'_'+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)
    

    sql="INSERT INTO `productos` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL,%s,%s,%s);"
    datos=(_nombre,nuevoNombre,_descarga)
    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_nombre)
    print(_descarga)
    print(_archivo)

    return redirect('/admin/licores')

@app.route('/admin/licores/borrar/', methods=['POST'])
def admin_licores_borrar():

    _id=request.form['txtID']
    print(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `productos`WHERE id=%s",(_id))
    licor=cursor.fetchall()
    conexion.commit()
    print(licor)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s",(_id))
    conexion.commit()
    return redirect('/admin/licores')

    

    
    
if __name__ == '__main__':
    app.run(debug=True)


