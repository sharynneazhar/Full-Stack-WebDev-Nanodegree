import webbrowser

class Media():
    def __init__(self, media_title, media_storyline, poster_image, trailer_youtube):
        self.title = media_title
        self.storyline = media_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

class Movie(Media):
    def __init__(self, movieData, movieReview):
        Media.__init__(self, movieData["title"], movieData["storyline"],
                       movieData["poster"], movieData["trailer"])
        self.movie_review = movieReview
