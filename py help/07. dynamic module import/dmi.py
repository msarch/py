class Scene(object):
    "Collects all actors in scene folder"

    def __init__(self, folder='', duration=0):
        self.actor_register = []
        self.folder = folder
        self.duration = duration

    def tick(self,dt):
        for actor in self.actor_register:
            actor.tick(dt)

    def paint(self):
        for actor in self.actor_register:
            actor.paint()

    def configure(self):
        #import all py files in self.folder
        os.chdir(self.folder)
        for filename in glob("*.py"):
            curdir = os.path.dirname(os.path.abspath(__file__))
            mysubdir= "/".join((curdir,self.folder))
            actor_file= "/".join((mysubdir,filename))
            new_actor = load_source(filename,actor_file)
            if hasattr(new_actor, 'register'):
                self.actor_registr.append(new_actor.register())
