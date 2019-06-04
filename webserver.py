#!/usr/bin/env python3
#
# The *hello server* is an HTTP server that responds to a GET request by
# sending back a friendly greeting.  Run this program in your terminal and
# access the server at http://localhost:8000 in your browser.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # First, send a 200 OK response.
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)

                # Then send headers.
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Now, write the response body.
                message = '''
                <html>
                    <head>
                        <title> Home </title>
                    </head>
                    <body>
                        <form action="/restaurants/new" method="POST">
		                <label>Resturant Name:
			                <input type="text" name="restaurant" value="">
			                <button type="submit">Add Resturant!</button>
		                </label>
	                    </form>
                    </body>
                </html>
                '''

                self.wfile.write(message.encode())

            if self.path.endswith("/restaurants"):
                self.send_response(200)

                # Then send headers.
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Now, write the response body.

                last = ""
                test = session.query(Restaurant).all()
                for t in test:
                    list = '<li>{:<10} <a style="text-decoration:none" href="{}/edit">Edit </a><a style="text-decoration:none" href="{}/delete">Delete</a> </li>'.format(t.name, t.id, t.id)
                    last += "{}\n".format(list)

                message = '''
                                <html>
                                    <head>
                                        <title> Restaurants </title>
                                        
                                    </head>
                                    <body>
                                        <a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>
                                        <h1> List of Resturants </hi>
                                        <div id="rest">
                                            <ul  style="font-weight:10;">
                                            {}
                                            </ul>
                                        </div>
                                    </body>
                                </html>
                                '''.format(last)

                self.wfile.write(message.encode())

            if self.path.endswith("/delete"):

                id = self.path.split("/")[1]
                print(id)

                rest = session.query(Restaurant).filter(Restaurant.id == id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                message = '''
                                <html>
                                    <head>
                                        <title> Delete </title>
                                    </head>
                                    <body>
                                        <form action="delete" method="POST">
                		                <label>Are you sure you want to delete {}
                			                <button type="submit">Delete</button>
                		                </label>
                	                    </form>
                                    </body>
                                </html>
                                '''.format(rest.name)
                self.wfile.write(message.encode())


            if self.path.endswith("/edit"):
                id = self.path.split("/")[1]
                print(id)

                rest = session.query(Restaurant).filter(Restaurant.id == id).one()

                self.send_response(200)

                # Then send headers.
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()


                # Now, write the response body.
                message = '''
                                <html>
                                    <head>
                                        <title> Rename Restaurant</title>
                                    </head>
                                    <body>
                                        <form action="edit" method="POST">
                		                <label>
                			                <input type="text" name="restaurant" value="{}">
                			                <button type="submit">Rename</button>
                		                </label>
                	                    </form>
                                    </body>
                                </html>
                                '''.format(rest.name)

                self.wfile.write(message.encode())
        except:
            pass



    def do_POST(self):
        if self.path.endswith("/restaurants/new"):
            length = int(self.headers.get('Content-length', 0))
            body = self.rfile.read(length).decode()
            params = parse_qs(body)['restaurant']
            print(str(params[0]).title())
            resturant_new = Restaurant(name=str(params[0]).title())
            session.add(resturant_new)
            session.commit()

        if self.path.endswith("/edit"):
            name = unquote(self.path)
            test = [char for char in name if char.isnumeric()]
            id = int("".join(test))
            print(id)

            length = int(self.headers.get('Content-length', 0))
            body = self.rfile.read(length).decode()
            params = parse_qs(body)['restaurant']
            print(str(params[0]).title())

            rest = session.query(Restaurant).filter(Restaurant.id == id).one()
            rest.name = str(params[0]).title()
            session.commit()

        if self.path.endswith("/delete"):
            name = unquote(self.path)
            test = [char for char in name if char.isnumeric()]
            id = int("".join(test))
            print(id)

            rest = session.query(Restaurant).filter(Restaurant.id == id).one()
            session.delete(rest)
            session.commit()

        self.send_response(303)
        self.send_header('Location', '/restaurants')
        self.end_headers()






def resturants():
    test = session.query(Restaurant).all()
    for t in test:
        print(str(t.name))



if __name__ == '__main__':
    resturants()
    server_address = ('', 8500)  # Serve on all addresses, port 8000.
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()

