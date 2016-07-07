import cgi
import query

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

                content = ""
                restaurants = query.restaurants()
                for restaurant in restaurants:
                    content += '''
                        <h2>{name}</h2>
                        <a href='/restaurants/{id}/edit'>Edit</a>
                        <a href='/restaurants/{id}/delete'>Delete</a>
                    '''.format(name=restaurant.name, id=restaurant.id)

                output = '''
                    <html><body>
                        <a href='/restaurants/new'>Make a New Restaurant Here</a>
                        %s
                    </body></html>
                ''' % content

                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = '''
                    <html><body>
                    <h2>Make a Restaurant</h2>
                    <form method='POST' enctype='multipart/form-data' action='restaurants/new'>
                        <input name='newRestaurantName' type='text' placeholder='New Restaurant Name' />
                        <input type='submit' value='Create' />
                    </form>
                    </body></html>
                '''

                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantId = self.path.split("/")[2]
                restaurant = query.restaurants_by_id(restaurantId)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = '''
                        <html><body>
                            <h2>%s</h2>
                            <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>
                                <input type='text' name='newRestaurantName' placeholder='%s' />
                                <input type='submit' value='Rename' />
                            </form>
                        </body></html>
                    ''' % (restaurant.name, restaurantId, restaurant.name)

                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                restaurantId = self.path.split("/")[2]
                restaurant = query.restaurants_by_id(restaurantId)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = '''
                        <html><body>
                            <h2>Are you sure you want to delete %s?</h2>
                            <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>
                                <input type='submit' value='Delete' />
                            </form>
                        </body></html>
                    ''' % (restaurant.name, restaurantId)

                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    param = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=param[0])
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
                    param = fields.get('newRestaurantName')

                    restaurantId = self.path.split("/")[2]
                    restaurant = session.query(Restaurant)\
                        .filter_by(id=restaurantId)\
                        .one()

                    if restaurant:
                        restaurant.name = param[0]
                        session.add(restaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                restaurantId = self.path.split("/")[2]
                restaurant = session.query(Restaurant)\
                    .filter_by(id=restaurantId)\
                    .one()

                if restaurant:
                    session.delete(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print '# Web server started...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '# Shutting down server...'
        server.socket.close()

if __name__ == '__main__':
    main()
