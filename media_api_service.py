import requests

API_KEY = '?api_key=656e04397adbf45701200273c181f445'
BASE_URL = 'https://api.themoviedb.org/3/'

def getMedia(media_type, media_id):
    """Get the list of movies from the API"""

    mediaURL = BASE_URL + media_type + "/" + str(media_id) + API_KEY
    videoURL = BASE_URL + media_type + "/" + str(media_id) + '/videos' + API_KEY

    # get the data from the API
    headers = {'Accept': 'application/json'}
    media_request = requests.get(mediaURL, headers=headers)
    video_request = requests.get(videoURL, headers=headers)

    # parse to json array
    media_response = media_request.json()
    video_response = video_request.json()

    # pull out desired attributes from json data
    data = {
        'poster': 'http://image.tmdb.org/t/p/w500' + media_response["poster_path"],
        'title': media_response["title"],
        'storyline': media_response["overview"],
        'trailer': 'https://www.youtube.com/watch?v=' + video_response["results"][0]["key"]
    }

    return data

def getMovieReviews(media_id):
    """Gets the movie review percentage from the API"""

    mediaURL = BASE_URL + "movie/" + str(media_id) + API_KEY

    headers = {'Accept': 'application/json'}
    media_request = requests.get(mediaURL, headers=headers)
    media_response = media_request.json()
    
    return (media_response["vote_average"])
