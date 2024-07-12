from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Movie:
    _id: str
    title: str
    director: str
    cast: str
    imdb_rating: str
    release_date: str
    genre: str
    runtime: str
    plot: str
    rated: str
    poster_url: str