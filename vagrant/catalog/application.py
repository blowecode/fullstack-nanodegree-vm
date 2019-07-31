from flask import Flask, render_template, request, url_for, jsonify, flash
from flask import session as login_session, make_response, redirect
import random
import string
from database_setup import Genre, Movie, Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Function to create a session for each database operation
def create_session():
    engine = create_engine('sqlite:///movieswithusers.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


# Returns API endpoint for movies for a specific genre
@app.route('/main/<int:genre_id>/movies/JSON')
def moviesForGenreJSON(genre_id):
    session = create_session()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(
        genre_id=genre_id).all()
    return jsonify(movies=[m.serialize for m in movies])


# Returns API endpoint for one specific movie
@app.route('/main/<int:genre_id>/movies/<int:movie_id>/JSON')
def movieJSON(genre_id, movie_id):
    session = create_session()
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(movie=movie.serialize)


# Returns API endpoint for a specific genre
@app.route('/JSON')
@app.route('/main/JSON')
def genresJSON():
    session = create_session()
    genres = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genres])


# Returns API endpoint for all movies in database
@app.route('/movies/JSON')
def moviesJSON():
    session = create_session()
    movies = session.query(Movie).all()
    return jsonify(movies=[m.serialize for m in movies])


def generateState():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    return state


@app.route('/login')
def showLogin():
    state = generateState()
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

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
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    session = create_session()
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    session = create_session()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        session = create_session()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url += login_session['access_token']
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
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
                    json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/main')
def displayGenres():
    session = create_session()
    genres = session.query(Genre)
    if 'username' in login_session:
        return render_template('main.html', genres=genres)
    else:
        return render_template('publicMain.html', genres=genres)


@app.route('/main/<int:genre_id>/')
@app.route('/main/<int:genre_id>/movies/')
def displayMovies(genre_id):
    session = create_session()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    creator = getUserInfo(genre.user_id)
    if 'user_id' in login_session and creator.id == login_session['user_id']:
        return render_template('displayMovies.html', genre=genre,
                               movies=movies)
    return render_template('publicDisplayMovies.html',
                           genre=genre, movies=movies)


@app.route('/main/<int:genre_id>/movies/<int:movie_id>/')
def displayMovie(genre_id, movie_id):
    session = create_session()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movie).filter_by(id=movie_id).one()
    creator = getUserInfo(genre.user_id)
    if 'user_id' in login_session and creator.id == login_session['user_id']:
        return render_template('displayMovie.html', movie=movie, genre=genre)
    return render_template('publicDisplayMovie.html', movie=movie, genre=genre)


@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    editedGenre = session.query(Genre).filter_by(id=genre_id).one()
    if editedGenre.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized\
                to edit this item.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            session.add(editedGenre)
            session.commit()
            return redirect(url_for('displayGenres'))
    else:
        return render_template('editGenre.html', genre=editedGenre)


@app.route('/main/new', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    if request.method == 'POST':
        newGenre = Genre(name=request.form['name'],
                         user_id=login_session['user_id'])
        session.add(newGenre)
        session.commit()
        return redirect(url_for('displayGenres'))
    else:
        return render_template('newGenre.html')


@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    deletedGenre = session.query(Genre).filter_by(id=genre_id).one()
    deletedMovies = session.query(Movie).filter_by(genre_id=genre_id).all()
    if editedGenre.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized\
                to edit this item.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(deletedGenre)
        for movie in deletedMovies:
            session.delete(movie)
        session.commit()
        return redirect(url_for('displayGenres'))
    else:
        return render_template('deleteGenre.html', genre=deletedGenre)


@app.route('/genre/<int:genre_id>/movies/<int:movie_id>/edit/',
           methods=['GET', 'POST'])
def editMovie(genre_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    editedGenre = session.query(Genre).filter_by(id=genre_id).one()
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    if editedMovie.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized '
                + 'to edit this item.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedMovie.name = request.form['name']
            session.add(editedMovie)
            session.commit()
            return redirect(url_for('displayMovie', genre_id=genre_id,
                                    movie_id=movie_id))
    else:
        return render_template('editMovie.html', genre=editedGenre,
                               movie=editedMovie)


@app.route('/genre/<int:genre_id>/new', methods=['GET', 'POST'])
def newMovie(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        newMovie = Movie(name=request.form['name'],
                         rating=request.form['rating'],
                         score=request.form['score'],
                         description=request.form['description'],
                         genre=genre,
                         user_id=login_session['user_id'])
        session.add(newMovie)
        session.commit()
        return redirect(url_for('displayMovies', genre_id=genre.id))
    else:
        return render_template('newMovie.html', genre=genre)


@app.route('/genre/<int:genre_id>/movies/<int:movie_id>/delete',
           methods=['GET', 'POST'])
def deleteMovie(genre_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    deletedMovie = session.query(Movie).filter_by(id=movie_id).one()
    if deletedMovie.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized\
                to edit this item.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(deletedMovie)
        session.commit()
        return redirect(url_for('displayMovies', genre_id=genre.id))
    else:
        return render_template('deleteMovie.html', genre=genre,
                               movie=deletedMovie)


@app.route('/main/movies')
def displayAllMovies():
    session = create_session()
    movies = session.query(Movie).all()
    return render_template("displayAllMovies.html", movies=movies)


if __name__ == '__main__':
    app.secret_key = '_esjpev7umhvU8J8zlvDnLDb'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
