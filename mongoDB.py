#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

# Conectar con la BD
def openRestaurantDB():
    # Connected service mongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Connected DB
    db = client['restaurant']

    # Get Collection (Table)
    dataCollections = db.restaurants
    return dataCollections

# Conectar con la BD
def openUserDB():
    # Connected service mongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Connected BD
    db = client['users']

    # Get Collection (Table)
    dataCollections = db.users
    return dataCollections

# Obtener lista de restaurantes en la BD
def getListRestaurant():
    # Open conex resturant BD
    dataRest = openRestaurantDB()

    # Get all list resturant
    listRest = dataRest.find()
    return listRest

# Obtener lista de restaurantes en la BD
def getListRestaurantPagination(pageNumber):
    # Open conex resturant BD
    dataRest = openRestaurantDB()

    # Numero de elementos por pagina
    rowPerPage = 15

    # Obtiene resultados desde la posicion de skip con un limite de 20 resultados
    listRest = dataRest.find().skip((int(pageNumber) - 1) * rowPerPage).limit(rowPerPage)
    return listRest

# Obtiene el numero de elementos totales en la BD y calcula numero de paginas en paginacion
def getNumTotalRestaurant():
    # Open conex restaurant BD
    dataRest = openRestaurantDB()

    # Numero de elementos por pagina
    rowPerPage = 15

    # Cuenta el numero de elementos totales en la BD y divide por el numero de elementos
    # por pagina para obtener cuantas paginas apareceran en la paginacion
    numResult = dataRest.find().count() / rowPerPage
    return numResult

# Obtener registro BD
def searchRestaurant(idr):
    # Get Collection (Table Restaurant)
    dataRest = openRestaurantDB()

    # Buscamos restaurante por id
    queryRest = dataRest.find_one({ "restaurant_id": idr })
    return queryRest

# Actualizar registro BD
def updateRestaurant(idr, name, city, street, zipcode):
    # Get Collection (Table Restaurant)
    dataRest = openRestaurantDB()

    # Actualizamos restaurante por id
    dataRest.update({ "restaurant_id": idr }, { "restaurant_id": idr, "name": name, "borough": city,   "address": { "street": street, "zipcode": zipcode } })
    #dataRest.update({ "restaurant_id": idr }, { $set: { "restaurant_id": idr, "name": name, "borough": city, "address": { "street": street, "zipcode": zipcode } }})

# Eliminar registro BD
def removeRestaurant(idr):
    # Get Collection (Table Restaurant)
    dataRest = openRestaurantDB()

    # Eliminamos restaurante por id
    dataRest.remove( { "restaurant_id": idr } )

# Insertar user BD
def newUser(name, email, passw):
    # Get Collection (Table User)
    dataUser = openUserDB()

    # Create user
    usuario = { "nombre": name, "email": email, "password": passw }

    # Insert User in Collection
    dataUser.insert(usuario)

# Obtener registro BD
def getUser(email):
    # Get Collection (Table User)
    dataUser = openUserDB()

    queryUser = dataUser.find_one({ "email": email })

    return queryUser

# Obtener registro BD
def searchUser(email, passw):
    # Get Collection (Table User)
    dataUser = openUserDB()

    # Buscamos usuario por email y password
    queryUser = dataUser.find_one({ "email": email, "password": passw })
    return queryUser

# Actualizar registro BD
def updateUser(name, email, passw):
    # Get Collection (Table Restaurant)
    dataUser = openUserDB()

    # Actualizamos restaurante por id
    dataUser.update({ "email": email }, { "nombre": name, "email": email, "password": passw })


# METODOS PARA Estadisticas
# Obtiene los 10 restaurantes mas votados
def getMoreVoted():
    # Open conex restaurant BD
    dataRest = getListRestaurant()

    # Init variables
    dataVoted = []
    pA = 0
    pB = 0
    pC = 0

    # Recorremos objeto restaurantes
    for data in dataRest:
        # A cada restaurante recorremos sus votos y calculamos
        for i in range(0, len(data['grades'])):
            # Segun grado de voto sumamos en una puntuacion u otra
            if data['grades'][i]['grade'] == 'A':
                pA += data['grades'][i]['score']
            elif data['grades'][i]['grade'] == 'B':
                pB += data['grades'][i]['score']
            else:
                pC += data['grades'][i]['score']

        #Create and append list of list restaurant
        dataVoted.append(list((data['name'], pA, pB, pC)))

    # Sort restaurant for moreVoted column pA
    dataVoted.sort(reverse=True, key = lambda row: row[1])

    # Truncate list of list 10 first element
    del dataVoted[10:]
    return dataVoted

# Obtiene numero total de restaurantes segun tipo cocina
def getCountRestCuisine():
    # Open conex restaurant BD
    dataRest = getListRestaurant()

    # Lista contendra el numero de restaurantes que hay por tipo de cocina
    listRest = []

    # Recorremos objeto restaurantes
    for data in dataRest:
        # Obtenemos tipo cocina del restaurante consultado
        cuisine = data['cuisine']

        # Si el tipo de cocina no se encuentra en la lista
        if cuisine not in listRest:
            nTotal = countTypeCuisine(cuisine=cuisine)

            # Añadimos tipo de cocina y el numero total de restaurantes
            #listRest.append(list((cuisine, numTotal)))
            listRest.extend((cuisine, nTotal))

    # Truncate list of list 10 first element
    #del listRest[16:]
    return listRest

# Cuenta el numero de restaurantes totales segun tipo de cocina
def countTypeCuisine(cuisine):
    # Open conex restaurant BD
    dataRest = getListRestaurant()

    # Init
    numTotal = 0

    # Consultamos todos los restaurantes de la lista y calculamos
    # cuantos restaurantes hay por tipo de cocina
    for data in dataRest:
        # Si tipo de cocina del restaurante consultado == cocina sumamos 1
        if cuisine == data['cuisine']:
            numTotal += 1

    return numTotal
