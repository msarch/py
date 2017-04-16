

# If you need to import modules not known in advance
# (i.e. as plugins, sort of), you can use this:

import os, glob, imp
modules = {}
for path in glob.glob('scene/[!_]*.py'):
    name, ext = os.path.splitext(os.path.basename(path))
    modules[name] = imp.load_source(name, path)


print modules

# Note :
# glob.glob('mypackage/[!_]*.py') will only return
# .PY files not starting with '_'.
