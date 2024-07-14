from flask import Blueprint, render_template, session, redirect, request, flash, url_for, current_app
from movie_library.form import MovieForm, RegisterForm, LoginForm
import requests, uuid
from movie_library.models import Movie, User
from passlib.hash import pbkdf2_sha256
from dataclasses import asdict



pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    movie_data = current_app.db.movie_details.find({})
    movies = [Movie(**movie) for movie in movie_data]
    return render_template(
        "index.html",
        title="Movies Watchlist",
        movies_data=movies
    )

@pages.route("/register", methods=["GET","POST"])
def register():
    if session.get("email"):
        return redirect(url_for("pages.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )
        current_app.db.user.insert_one(asdict(user))
        flash("User registered successfully", "success")
        return redirect(url_for("pages.login"))

    return render_template("register.html", title="Movie Watchlist - Register", form=form)

@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for("pages.index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for("pages.login"))
        user = User(**user_data)

        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect(url_for("pages.index"))
        
        flash("Login credentials not correct", category="danger")
    return render_template("login.html", title="Movies Watchlist - Login", form=form)

@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie_name = form.title.data
        api_url = f"https://www.omdbapi.com/?t={movie_name}&apikey=ddd3c2a0"
        response = requests.get(api_url)
        if response.status_code == 200:
            
            movie_data = response.json()
            if movie_data['Response'] == 'True':
                movie = Movie(
                    _id = uuid.uuid4().hex,
                    title = movie_name,
                    director = movie_data.get('Director', 'N/A'),
                    cast =  movie_data.get('Actors', 'N/A'),
                    imdb_rating = movie_data.get('imdbRating', 'N/A'),
                    release_date =  movie_data.get('Released','N/A'),
                    genre = movie_data.get('Genre','N/A'),
                    runtime = movie_data.get('Runtime','N/A'),
                    plot = movie_data.get('Plot','N/A'),
                    rated = movie_data.get('Rated','N/A'),
                    poster_url = movie_data.get('Poster','N/A')
                )
                current_app.db.movie_details.insert_one(asdict(movie))             
                flash(f"Movie Added, Successfully!", 'success')
                return redirect(url_for('pages.add_movie'))
            else:
                flash(f"Error: {movie_data.get('Error', 'Movie not found.')}", 'danger')
                return redirect(url_for('pages.add_movie'))
                
        else:
            flash(f"Error: Unable to fetch data from OMDb API. Status code: {response.status_code}", 'danger')
            return redirect(url_for('pages.add_movie'))
        
    
            
    return render_template("new_movie.html", title="Movies Watchlist -- Add Movie", form=form)


@pages.get("/movie/<string:_id>")
def movie(_id: str):
    movie_data = current_app.db.movie_details.find_one({"_id": _id})
    if movie_data is not None:
        movie = Movie(**movie_data)
        return render_template("movie_details.html", movie=movie)
    else:
        flash("Movie not found", "danger")
        return redirect(url_for('pages.index'))

@pages.route("/delete/<string:_id>", methods=["POST"])
def delete_movie(_id: str):
    current_app.db.movie_details.delete_one({"_id": _id})
    return redirect(url_for('pages.index'))

@pages.get("/toggel-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    
    return redirect(request.args.get("current_page"))