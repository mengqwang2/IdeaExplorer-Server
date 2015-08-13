import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import onlineIdea
import tagGen

# Generate lambda, gamma and Tag set in the data file
# For the parameter, please refer to tagGen and onlineIdea
def main():
    tagGen.TagGen(docNum = 5000).generateAllTags()
    onlineIdea.IdeaLDA(batchsize = 50,d = 5000 ,k = 100 ,tau = 1024 ,kappa = 0.7).runLDA()

if __name__ == '__main__':
    main()
