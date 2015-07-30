# IdeaExplorer-Server

#Installation Guide
1. Configure include path:
find </microblog/IdeaExplorer-Server> -type f -exec sed -i -e 's|<Users/mengqwang/Documents/IdeaExplorer/Idea-Server>|<microblog/IdeaExplorer-Server>|g' {} \;

2. Configure DB:
__init__.py

app.config["MONGODB_HOST"] = "10.43.77.30"
app.config["MONGODB_PORT"] = 27017
app.config["MONGODB_DB"] = "tumblelog"

