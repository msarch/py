#As mentioned the imp module provides you loading functions.

#imp.load_source(path)

#imp.load_compiled(path)

#I've used these before to perform something similar.
#In my case I defined a specific class with defined methods that were required. So, once I loaded the module I would check if the class was in the module, and then create an instance of that class.

#Something like this:

import imp
import os

def load_from_file(filepath):
    class_inst = None
    expected_class = 'MyClass'

    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expected_class):
        class_inst = py_mod.MyClass()

    return class_inst
