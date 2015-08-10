import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+'/IdeaExplorer/LDA')
import onlineIdea
import tagGen

def main():
    tagGen.TagGen(docNum = 50).generateAllTags()
    onlineIdea.IdeaLDA(batchsize = 5,d = 50 ,k = 10 ,tau = 1000 ,kappa = 0.7).runLDA()

if __name__ == '__main__':
    main()
