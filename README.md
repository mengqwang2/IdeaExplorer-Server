# IdeaExplorer-Server

# Server Installation
1. Configure DB:
Clone all the data from the original test DB server


2. Configure Web Server:
__init__.py

app.config["MONGODB_HOST"] = <DB server IP>
app.config["MONGODB_PORT"] = 27017
app.config["MONGODB_DB"] = "tumblelog"


3. Try http://localhost:5000 for the prototype
Port 5000 has all the functionalities that the mobile app has for testing


#System Design
The Topic Modeling algorithm is based on the online LDA proposed by M. Hoffman. The paper and Python implementation can be found at: https://www.cs.princeton.edu/~blei/topicmodeling.html

The database design is illustrated as schemas in models.py


