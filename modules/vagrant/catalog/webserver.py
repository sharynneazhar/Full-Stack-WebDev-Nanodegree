from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import cgi
import query

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href=\"/restaurants/new\">Add a new restaurant</a>"

                results = query.restaurants()
                for item in results:
                    output += '''
                        <div>
                            <h3>{name}</h3>
                            <a href=\"/restaurants/%s/edit\">Edit </a>"
                            <a href=\"#\">Delete</a>
                        </div>
                    '''.format(name=item[0]) % restaurant.id

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += '''
                    <html>
                        <body>
                            <h2>Add a new restaurant</h2>
                            <form action=\"/restaurants/new\" method=\"POST\" enctype=\"multipart/form-data\">
                                <input type=\"text\" name=\"newRestaurantName" />
                                <input type=\"submit\" value=\"Add\" />
                            </form>
                        </body>
                    </html>
                '''
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if restaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurantQuery.name
                    output += "</h1>"
                    output += '''
                        <form method=\"POST\" enctype=\"multipart/form-data\" action=\"/restaurants/%s/edit\">
                            <input name=\"newRestaurantName\" type=\"text\" placeholder=\"%s\"> 
                            <input type=\"submit\" value=\"Rename\">
                        </form>
                    ''' % (restaurantIDPath, restaurantQuery.name)
                    output += "</body></html>"

                    self.wfile.write(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get("newRestaurantName")

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    restaurantQuery = query.restaurants_by_id(restaurantIDPath)
                    if restaurantQuery != []:
                        restaurantQuery.name = messagecontent[0]
                        session.add(restaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
