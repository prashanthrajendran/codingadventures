# Create your views here.
from TicketBooking.models import Movie
from django.http import HttpResponse
import collections
import jsonpickle

def movie_list(request):
    movies = Movie.objects.select_related(depth=1).all()
    movieHash = collections.defaultdict(list)
    class movieDetails:
        language = ''
        movies = []
        def __init__(self,language,movies):
            self.language = language
            self.movies = movies
    for m in movies:
        movieHash[m.language.name].append(m.movie)
    movieList = []
    for m in movieHash:
        mv = movieDetails(language=m,movies=movieHash[m])
        movieList.append(mv)
    json = jsonpickle.encode(movieList,unpicklable=False)
    return HttpResponse(json, mimetype="application/json")
