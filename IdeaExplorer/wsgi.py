import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from IdeaExplorer import app

if __name__ == "__main__":
	app.run()