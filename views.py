# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect, flash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask.ext.httpauth import HTTPBasicAuth
import json

from database_setup import Base, User, FoodClass, FoodItem

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

auth = HTTPBasicAuth()

app = Flask(__name__)

engine = create_engine('sqlite:///foodlist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


#The API-Endpoints (GET-Request)
@app.route('/foodclass/<int:foodclass_id>/food/JSON')
def foodclassFoodJSON(foodclass_id):
    foodclass = session.query(FoodClass).filter_by(id=foodclass_id).one()
    items = session.query(FoodItem).filter_by(foodclass_id=foodclass.id).all()
    return jsonify(FoodItems=[i.serialize for i in items])

@app.route('/foodclass/<int:foodclass_id>/food/<int:food_id>/JSON')
def foodclassFoodItemJSON(foodclass_id, food_id):
    item = session.query(FoodItem).filter_by(id=food_id, foodclass_id=foodclass_id).one()
    return jsonify(FoodItem=item.serialize)


@app.route('/foodclasses/JSON')
def foodclassesJSON():
    foodclasses = session.query(FoodClass).all()
    return jsonify(foodclasses= [r.serialize for r in foodclasses])


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token => mit jedem neuen Login wird dem User ein anderer Token zugeordnet - welcher hilft, den Nutzer als er selbst zu identifizieren
@app.route('/login')
def showLogin():
    #Random String generieren (mit Großbuchstaben und Zahlen)
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    #diesen String in der login-session als state speichern
    login_session['state'] = state
    #render login_template
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token - if that token is invalid it will stop talking to the client (thus protecting it and the server)
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data #der komplette id_token mit allen Infos

    # check des id_token gegen die client_secrets Daten
    from oauth2client import client, crypt
    try:
        idinfo = client.verify_id_token(code, CLIENT_ID)
        #auf korrekten issuer prüfen
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            response = make_response(
            json.dumps("Wrong issuer."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        #gplus-ID rausfischen
        gplus_id = idinfo['sub']
    except crypt.AppIdentityError:
        # Verify that the access token is used for the intended user.
        userid = idinfo['sub']
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Online-Check that the id_token is valid. - returns a nice json-dic with the data in the token
    access_token = code
    url = ('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['aud'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    data = result

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, {}!</h1>'.format(login_session['username'])
    output += '<img src="{} " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '.format(login_session['picture'])
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


##Making the normal Webpage
@app.route('/')
@app.route('/catalog/')
def Catalog():
    foodclasses = session.query(FoodClass).all()
    #items = session.query(FoodItem).filter_by(foodclass_id=foodclass.id)
    return render_template('catalog.html', foodclasses = foodclasses)

@app.route('/Foodclasses/<int:foodclass_id>/')
def SingleFoodClass(foodclass_id):
    foodclass = session.query(FoodClass).filter_by(id=foodclass_id).one()
    items = session.query(FoodItem).filter_by(foodclass_id=foodclass.id).all()
    return render_template('Foodclass.html', foodclass = foodclass, items = items)

@app.route('/Foodclasses/NewClass/', methods=['GET', 'POST'])
def NewFoodClass():
  if 'username' not in login_session:
      return redirect('/login')
  if request.method == 'POST':
      foodclass = FoodClass(name = request.form['name'], creator_id=login_session['user_id'])
      session.add(foodclass)
      flash('New Foodclass %s Successfully Created' % foodclass.name)
      session.commit()
      return redirect(url_for('/catalog'))
  else:
      return render_template('newFoodClass.html')



## Task 1: Create route for newMenuItem function here
#@app.route('/restaurants//<int:restaurant_id>/new/', methods=['GET', 'POST']) # => Handling von GET & POST ermöglichen
#def newMenuItem(restaurant_id):
    #if request.method == 'POST':
        #newItem = MenuItem(name= request.form['name'], restaurant_id = restaurant_id)
        #session.add(newItem)
        #session.commit()
        #flash("new menu item created") # => adding a flash-message to the session (abgerufen werden sie in 'menu.html')
        #return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    #else:
        #return render_template('newMenuItem.html', restaurant_id = restaurant_id)

## Task 2: Create route for editMenuItem function here
#@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit',
           #methods=['GET', 'POST'])
#def editMenuItem(restaurant_id, MenuID):
    #editedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    #if request.method == 'POST':
        #if request.form['name']:
            #editedItem.name = request.form['name']
        #session.add(editedItem)
        #session.commit()
        #flash("menu item edited")
        #return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    #else:
        #return render_template(
            #'editMenuItem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=editedItem)


## Task 3: Create a route for deleteMenuItem function here
#@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
#def deleteMenuItem(restaurant_id, menu_id):
    #deletedItem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    #if request.method == 'POST':
        #session.delete(deletedItem)
        #session.commit()
        #flash("Menu item {} deleted".format(deletedItem.name))
        #return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    #else:
        #return render_template(
            #'deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)



if __name__ == '__main__':
    app.debug = True
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=8000)
