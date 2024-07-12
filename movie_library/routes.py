from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from movie_library.form import MovieForm
import requests


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    return render_template(
        "index.html",
        title="Movies Watchlist",
    )

@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()
    if request.method == "POST":
        movie_name = form.title.data
        api_url = f"https://www.omdbapi.com/?t={movie_name}&apikey=******"
        response = requests.get(api_url)
        if response.status_code == 200:
            movie_data = response.json()
            if movie_data['Response'] == 'True':
                cast = movie_data.get('Actors', 'N/A')
                director = movie_data.get('Director', 'N/A')
                imdb_rating = movie_data.get('imdbRating', 'N/A')
                release_date = movie_data.get('Released','N/A')
                genre = movie_data.get('Genre','N/A')
                runtime = movie_data.get('Runtime','N/A')

                flash(f"Movie Added, Successfully!", 'success')
                return redirect(url_for('pages.add_movie'))
            else:
                flash(f"Error: {movie_data.get('Error', 'Movie not found.')}", 'danger')
                return redirect(url_for('pages.add_movie'))
                
        else:
            flash(f"Error: Unable to fetch data from OMDb API. Status code: {response.status_code}", 'danger')
            return redirect(url_for('pages.add_movie'))
            
    return render_template("new_movie.html", title="Movies Watchlist -- Add Movie", form=form)

@pages.get("/toggel-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    
    return redirect(request.args.get("current_page"))