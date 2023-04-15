# Description: This file is the entry point for the server
# It is responsible for creating the server and adding the GraphQL endpoint to it.

#Import the needed libraries  
from flask import Flask
from strawberry.flask.views import GraphQLView
from schema.schema import schema

#Create the server
server = Flask(__name__)

#Add the GraphQL endpoint to the server
server.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

#Run the server
if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=5020,threaded=True)