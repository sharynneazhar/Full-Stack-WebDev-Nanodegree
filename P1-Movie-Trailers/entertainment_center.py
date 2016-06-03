import media_api_service as tmdbService
import media
import fresh_tomatoes

# list of movie ids found on TheMovieDatabase.org
FAVORITE_MOVIES = [293660, 150540, 424, 118340, 76341,
                   136795, 228967, 116741, 212778]

def getMovieById(movie_id):
    movieData = tmdbService.getMedia("movie", movie_id)
    movieReview = tmdbService.getMovieReviews(movie_id)
    movie = media.Movie(movieData, movieReview)
    return movie

movieList = []
for movie in FAVORITE_MOVIES:
    movieList.append(getMovieById(movie))

fresh_tomatoes.open_movies_page(movieList)
