#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, flash, Markup, session, redirect, jsonify
from bson.json_util import dumps
import os
import mongoDB
import feedParserRss
import tweepyTwitter

# Cambiamos la ruta de la carpeta template, para que el modulo render_template apunte a dicha carpeta
app = Flask(__name__, template_folder='web')

# Key secret de tipo string generada automaticamente con algoritmo urandom
app.secret_key = os.urandom(24)

# MANEJO DE URL EN LA WEB
@app.route('/')
def index():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        addUrlLastPage(url="/", email=session['email'])

    return render_template('index.html')

@app.route('/sobre_nosotros')
def about():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        addUrlLastPage(url="sobre_nosotros", email=session['email'])
    return render_template('about-me.html')

# Lista de restaurantes
@app.route('/restaurantes')
def restaurant():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        addUrlLastPage(url="restaurantes", email=session['email'])

    # Obtenemos de mongoDB la lista con todos los restaurantes de la BD
    dataRest = mongoDB.getListRestaurant()

    return render_template('restaurant.html', dataRest=dataRest)

# Tabla de restaurantes para modificar
@app.route('/lista_restaurantes')
def listRestaurant():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        addUrlLastPage(url="lista_restaurantes", email=session['email'])

        # Obtenemos de mongoDB la lista con todos los restaurantes de la BD
        dataRest = mongoDB.getListRestaurantPagination(pageNumber=1)

        # Obtenemos numero total de elementos a paginar
        numResult = mongoDB.getNumTotalRestaurant()
        return render_template('restaurant-list.html', dataRest=dataRest, numResult=numResult)
    else:
        return redirect(url_for('login'))

# Tabla de restaurantes para modificar
@app.route('/getpagination')
def restaurantPagination():
    # Obtenemos de mongoDB la lista con todos los restaurantes de la BD
    pageNumber = request.args.get('pageNumber')
    dataRest = mongoDB.getListRestaurantPagination(pageNumber=pageNumber)
    return dumps(dataRest)

@app.route('/restaurante', methods=['GET', 'POST'])
def modRestaurant():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        #OBTENEMOS DATOS DE URL
        idr = str(request.args.get('id'))

        # Obtenemos restaurante de la BD, a traves del id indicado
        dataRest = mongoDB.searchRestaurant(idr)

        # Comprobamos si la consulta ha devuelto un restaurante y no es consulta vacia
        if dataRest != None:
            # Redirigimos a seccion y pasamos sesion
            return render_template('update-restaurant.html', dataRest=dataRest)
        else:
            # Si el restaurante no existe, regresamos a la tabla de restaurantes
            return redirect(url_for('listRestaurant'))
    else:
        return redirect(url_for('login'))

# Obtener información de un restaurante "x"
@app.route('/info_restaurante')
def infoRestaurante():
    # Obtenemos id del restaurante pasado por url
    idr = request.args.get('id')

    # Obtenemos información del restuante en la BD
    dataRest = mongoDB.searchRestaurant(idr=idr)

    # Comprobamos si la consulta ha devuelto un restaurante y no es consulta vacia
    if dataRest != None:
        # Redirigimos a seccion y pasamos objeto restuante
        return render_template('info-restaurant.html', dataRest=dataRest)
    else:
        # Si el restaurante no existe, regresamos a la lista de restaurantes
        return redirect(url_for('listRestaurant'))

# Modificar datos de un restaurante "x"
@app.route('/modificar_restaurante', methods=['GET', 'POST'])
def updateRestaurant():
    # Comprobamos si los datos del formulario son vacios (Por seguridad evita acceso por URL)
    if request.form['id']:
        # Obtenemos datos POST del formulario y hacemos codificamos a UFT-8 para permitir acentos, caracteres extraños, etc.
        idr = request.form['id'].encode('utf_8')
        name = request.form['name'].encode('utf_8')
        city = request.form['city'].encode('utf_8')
        street = request.form['street'].encode('utf_8')
        zipcode = request.form['zipcode'].encode('utf_8')

        # Actualizamos registro en BD local
        mongoDB.updateRestaurant(idr=idr, name=name, city=city, street=street, zipcode=zipcode)
        return redirect(url_for('listRestaurant'))
    else:
        return redirect(url_for('listRestaurant'))

@app.route('/eliminar_restaurante', methods=['GET', 'POST'])
def removeRestaurant():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        #OBTENEMOS DATOS DE URL
        idr = str(request.args.get('id'))

        # Obtenemos restaurante de la BD, a traves del id indicado
        mongoDB.removeRestaurant(idr)
        return redirect(url_for('listRestaurant'))
    else:
        return redirect(url_for('login'))

@app.route('/iniciar_sesion')
def login():
    return render_template('login.html')

@app.route('/crear_cuenta')
def registro():
    return render_template('sing-up.html')

@app.route('/mi_perfil')
def miPerfil():
    # Comprobamos si la sesion esta activa (Por seguridad evita acceso por URL)
    if 'email' in session:
        # Obtenemos registro de BD local
        user = mongoDB.getUser(email=session['email'])

        # Añadimos url a las ultimas paginas visitadas de la sesion
        addUrlLastPage(url="mi_perfil", email=session['email'])

        return render_template('page-user.html', session=session, user=user)
    else:
        return redirect(url_for('index'))

# ERROR_404
@app.errorhandler(404)
def errorNotFound(error):
    return render_template('error404.html'), 404

# FORMULARIO DE REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def createUser():
    # Comprobamos si los datos del formulario son vacios (Por seguridad evita acceso por URL)
    if request.form['email']:
        # Obtenemos datos POST del formulario y hacemos codificamos a UFT-8 para permitir acentos, caracteres extraños, etc.
        name = request.form['name'].encode('utf_8')
        email = request.form['email'].encode('utf_8')
        passw = request.form['passw'].encode('utf_8')

        # Insertamos datos en BD local
        mongoDB.newUser(name=name, email=email, passw=passw)

        # Mostramos mensaje de confirmacion
        mensaje = 'correctCreateUser'
        return render_template('msg-form.html', msg=mensaje)
    else:
        return render_template('sing-up.html')


# MANEJO FORMULARIO DE REGISTRO
@app.route('/modificar_usuario', methods=['GET', 'POST'])
def updateUser():
    # Comprobamos si los datos del formulario son vacios (Por seguridad evita acceso por URL)
    if request.form['email']:
        # Obtenemos datos POST del formulario y hacemos codificamos a UFT-8 para permitir acentos, caracteres extraños, etc.
        name = request.form['name'].encode('utf_8')
        email = request.form['email'].encode('utf_8')
        passw = request.form['passw'].encode('utf_8')

        # Actualizamos registro en BD local
        mongoDB.updateUser(name=name, email=email, passw=passw)
        return redirect(url_for('miPerfil'))
    else:
        return redirect(url_for('miPerfil'))

# SESIONES
# Inicio Sesion
@app.route('/comprobar_user', methods=['GET', 'POST'])
def createSesion():
    # Comprobamos si los datos del formulario son vacios (Por seguridad evita acceso por URL)
    if request.form['email']:
        # Obtenemos datos POST del formulario y hacemos codificamos a UFT-8 para permitir acentos, caracteres extraños, etc.
        email = request.form['email'].encode('utf_8')
        passw = request.form['passw'].encode('utf_8')

        # Obtenemos datos de BD local, a traves del email indicado
        user = getDataUser(email, passw)

        # Comprobamos si la consulta ha devuelto un usuario y no es consulta vacia
        if user != None:
            # Creamos sesion, asignando email
            session['email'] = user['email']
            session['lastpage'] = []

            # Redirigimos a seccion y pasamos sesion
            return redirect(url_for('miPerfil'))
        else:
            # Mostramos mensaje de error
            mensaje = 'userNotFound'
            return render_template('msg-form.html', msg=mensaje)
    else:
        return redirect(url_for('login'))

# Cierre sesion
@app.route('/cerrar_sesion')
def clearSession():
    session.clear()
    #session.pop('email', None)
    return redirect(url_for('login'))

# Obtiene registros de la BD del usuario conectado
def getDataUser(email, passw):
    # Obtener usuario BD mongo
    usuario = mongoDB.searchUser(email=email, passw=passw)
    return usuario

# Añade las ultimas paginas visitas a la sesion
def addUrlLastPage(url, email):
    if 'lastpage' in session:
        session['email'] = email
        session['lastpage'].insert(0, url)

# Obtiene noticias de RSS y parseamos
@app.route('/noticias')
def rss():
    # Obtenemos objeto RSS parseado
    dataFeed = feedParserRss.getRSS()

    # Comprobamos si la consulta ha devuelto un informacion y no es consulta vacia
    #if dataFeed != None:
        # Redirigimos a seccion y pasamos objeto
    return render_template('noticias.html', dataFeed=dataFeed)

# Obtiene tweets a traves de Tweepy
@app.route('/twitter')
def tweets():
    # Obtenemos objeto RSS parseado
    dataTweet = tweepyTwitter.getTweets()

    # Comprobamos si la consulta ha devuelto un informacion y no es consulta vacia
    if dataTweet != None:
        # Redirigimos a seccion y pasamos objeto
        return render_template('twitter.html', dataTweet=dataTweet)

# Obtiene tweets a traves de Tweepy
@app.route('/twitter_estadisticas')
def mashupTweet():
    # Obtenemos objeto RSS parseado
    dataTweet = tweepyTwitter.getTweetsForHashtag()

    # Comprobamos si la consulta ha devuelto un informacion y no es consulta vacia
    if dataTweet != None:
        # Redirigimos a seccion y pasamos objeto
        return render_template('twitter_estadisticas.html', dataTweet=dataTweet)

# Estadisticas de resultados
@app.route('/estadisticas')
def estadisticas():
    # Obtenemos restaurantes mas votados
    dataMoreVoted = mongoDB.getMoreVoted()

    # Obtenemos numero total de restaurantes segun tipo cocina
    dataCountCuisine = mongoDB.getCountRestCuisine()

    # Redirigimos a seccion y pasamos objeto restuante
    return render_template('estadisticas.html', dataMoreVoted=dataMoreVoted, dataCountCuisine=dataCountCuisine)

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(host='0.0.0.0')
