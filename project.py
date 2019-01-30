from flask import Flask, render_template
from flask import request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Book Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///bookcatalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
                      string.ascii_uppercase + string.digits
                      ) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                    'Current user is already connected.'
                                            ),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['email']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
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


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show home page
@app.route('/')
def showHome():
    categories = session.query(Category).order_by(asc(Category.name))
    lastItems = session.query(CategoryItem).order_by(
                CategoryItem.id.desc()).limit(9)
    return render_template('home.html',
                           categories=categories, lastItems=lastItems)


# Show items list in the Category
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    category_items = session.query(CategoryItem).filter_by(
                     category_id=category_id).all()
    item_number = len(category_items)
    category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('itemslist.html',
                           category=category, items=category_items,
                           categories=categories, item_number=item_number)


# show item description
@app.route('/catalog/<int:item_id>/itemdescription')
def itemDescription(item_id):
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('itemdescription.html', item=item)


# add new item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = CategoryItem(title=request.form['title'],
                               description=request.form['description'],
                               category_id=request.form['category_id'],
                               user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("new item created successfully!")
        return redirect(url_for('showHome'))
    else:
        return render_template('newitem.html', categories=categories)


# edit items
@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    categories = session.query(Category).all()
    if login_session['user_id'] != item.user_id:
        return "You Are Not Authorized To Edit This Item"
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
            item.description = request.form['description']
            item.category_id = request.form['category_id']
            session.add(item)
            session.commit()
            flash("item data updated successfully!")
            return redirect(url_for('itemDescription', item_id=item.id))
    else:
        return render_template('edititem.html', item=item,
                               categories=categories)


# delete items
@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleted_item = session.query(CategoryItem).filter_by(id=item_id).one()
    if login_session['user_id'] != deleted_item.user_id:
        return "You Are Not Authorized To Delete This Item"
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        flash("item deleted successfully!")
        return redirect(url_for('showItems',
                        category_id=deleted_item.category_id))
    else:
        return render_template('deleteitem.html', item=deleted_item,
                               category_id=deleted_item.category_id)


# JSON APIs to view The Catalog Information
@app.route('/catalog/<int:item_id>/itemdetails/json')
def restaurantMenuJSON(item_id):
    item = session.query(CategoryItem).filter_by(
        id=item_id).one()
    return jsonify(ItemDetails=item.serialize)


@app.route('/catalog/<int:category_id>/items/json')
def categoryItemsJSON(category_id):
    items = session.query(CategoryItem).filter_by(
          category_id=category_id).all()
    return jsonify(Category_Items=[i.serialize for i in items])


@app.route('/catalog/categories/json')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
