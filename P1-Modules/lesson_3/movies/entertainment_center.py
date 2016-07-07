import media
import fresh_tomatoes

toy_story = media.Movie("Toy Story",
                        "A story of a boy and his toys that come to life",
                        "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=vwyZH85NQC4")

internship = media.Movie("The Internship",
                             "Two salesman who became interns at Google",
                             "https://upload.wikimedia.org/wikipedia/en/e/ed/The-internship-poster.jpg",
                             "https://www.youtube.com/watch?v=cdnoqCViqUo")

school_of_rock = media.Movie("School of Rock",
                             "Storyline",
                             "http://upload.wikimedia.org/wikipedia/en/1/11/School_of_Rock_Poster.jpg",
                             "https://www.youtube.com/watch?v=3PsUJFEBC74")

hangover = media.Movie("The Hangover",
                       "Four guys goes to Las Vegas",
                       "https://upload.wikimedia.org/wikipedia/en/b/b9/Hangoverposter09.jpg",
                       "https://www.youtube.com/watch?v=vhFVZsk3XEs")

heat = media.Movie("The Heat",
                    "An uptight FBI Agent paired with a foul-mouth Boston cop take down a ruthless drug lord",
                    "https://upload.wikimedia.org/wikipedia/en/b/bf/The_Heat_poster.jpg",
                    "https://www.youtube.com/watch?v=1O3iRdiplB0")

chef = media.Movie("Chef",
                    "A chef who loses his restauratn job starts up a food truck",
                    "https://upload.wikimedia.org/wikipedia/en/b/b8/Chef_2014.jpg",
                    "https://www.youtube.com/watch?v=mLuixZwiIdU")

interview = media.Movie("The Interview",
                        "A talk-show host and his producer lands an interview with North Korean dictator, Kim Jong-Un",
                        "https://upload.wikimedia.org/wikipedia/en/2/27/The_Interview_2014_poster.jpg",
                        "https://www.youtube.com/watch?v=frsvWVEHowg")

good_will = media.Movie("Good Will Hunting",
                                "Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life.",
                                "https://upload.wikimedia.org/wikipedia/en/b/b8/Good_Will_Hunting_theatrical_poster.jpg",
                                "https://www.youtube.com/watch?v=z02M3NRtkAA")

lion_king = media.Movie("The Lion King",
                        "Lion cub and future king Simba searches for his identity.",
                        "https://upload.wikimedia.org/wikipedia/en/3/3d/The_Lion_King_poster.jpg",
                        "https://www.youtube.com/watch?v=4sj1MT05lAA")

movies = [chef, heat, lion_king, internship, interview, good_will, toy_story, school_of_rock, hangover]
# fresh_tomatoes.open_movies_page(movies)
print (media.Movie.__doc__)
