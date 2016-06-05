import urllib.request
import re

def read_text() :
    quotes = open("movie_quotes.txt")
    contents = quotes.read()
    # print(contents)
    quotes.close()
    contents = re.sub(" ", "%20", contents)
    contents = re.sub("\n", "%20", contents)
    check_profanity(contents)

def check_profanity(text) :
    connection = urllib.request.urlopen("http://www.wdylike.appspot.com/?q=" + text)
    output = connection.read()
    print(output)
    connection.close()

read_text()
