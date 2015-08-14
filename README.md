# IdeaExplorer-Server
IdeaExplorer is an intelligent mobile platform for idea collaboration in EMC. Users can browse the innovations through a simple keyword search and further provide their comments and ratings for each innovation on the platform. The platform is smart in that it reduces the dimension of innovation documents so that words can be mapped to documents in the statistical manner. It can further automatically recommend relevant innovations to the users according to users' preference and browsing history. 

Checking out the full demo of this amazing application here: https://www.youtube.com/watch?v=14AU8FYZVO8


We shot this video when we delopyed the application as a micro-service on Rasperry Pi and won the runner-up in the EMC Pi Hackathon.


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
The Topic Modeling algorithm is based on the online LDA proposed by M. Hoffman. The paper and Python implementation can be found at: https://www.cs.princeton.edu/~blei/topicmodeling.html. For detail about implemention of the model, please check the readme.txt file in IdeaExplorer/LDA.

The database design is illustrated as schemas in models.py

# Database Installation
Mongo DB and flask need to be installed first. 

The original idea.txt file needs to be put in IdeaExplorer/Data where fieldflist.txt and vocabulary.txt have already been stored.

Run CreateData.py to create part of results stored in IdeaExplorer/Data.(the step of training the model) Then run DBGen.py to get some other data generated and all the data will be stored in Mongo DB. The latter one may take a long time. (depends on the size of data, might take more than an hour) 

# To do list
The ionic App is the latest version, however, the page of web server has not been updated and is still an old version. It needs to be updated if one wants to view the webpage without ionic.

The parameters used in the algorithm may be modified to attain a better result. For detail, see the readme.txt in LDA.

An adminster page can be written to get an overview of the whole information of data. 

After collecting the data of users' behaviour, more functions could be generated to make further analysis. 

The present database cannot be updated automatically. Celery may be used to make the database updated everyday and automatically.
