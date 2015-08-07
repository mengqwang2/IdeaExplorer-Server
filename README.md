# IdeaExplorer-Server
IdeaExplorer is an intelligent mobile platform for idea collaboration in EMC. Users can browse the innovations through a simple keyword search and further provide their comments and ratings for each innovation on the platform. The platform is smart in that it reduces the dimension of innovation documents so that words can be mapped to documents in the statistical manner. It can further automatically recommend relevant innovations to the users according to users' preference and browsing history. 

This repository is created for the server implementation while there is another repository for the front-end ionic implementation.



# Server Installation
Configure DB
--------------
Clone all the data from the original test DB server


Configure Web Server
--------------

__init__.py

- app.config["MONGODB_HOST"] = DB server IP
- app.config["MONGODB_PORT"] = 27017
- app.config["MONGODB_DB"] = "tumblelog"


Try http://localhost:5000 for the prototype
--------------
Port 5000 has all the functionalities that the mobile app has for testing


#System Design
The Topic Modeling algorithm is based on the online LDA proposed by M. Hoffman. The paper and Python implementation can be found at: https://www.cs.princeton.edu/~blei/topicmodeling.html

The database design is illustrated as schemas in models.py


