import os
from glob import glob
from imp import load_source
import os, glob, imp

class Scene(object):

    def __init__(self, folder=None):
        self.folder_name=folder
        self.fl=[] # file list
        self.actor_registry = []
        self.rule_registry = []

    #---dynamic scene handling ------------------------------------------------
        modules = {}
        for path in glob.glob('scene/[!_]*.py'):
            name, ext = os.path.splitext(os.path.basename(path))
            modules[name] = imp.load_source(name, path)
        print modules


##---MAIN----------------------------------------------------------------------

def main():
    scene1= Scene(folder='scene')


##-----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
