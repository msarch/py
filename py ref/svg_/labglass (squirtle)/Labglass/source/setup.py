# To change this template, choose Tools | Templates
# and open the template in the editor.


from distutils.core import setup
import py2exe

setup(
version = '1.0',
console=['labglass.py'],
options = {
                  'py2exe': {
                      'packages':'encodings',
                      'includes': 'cairo, pango, pangocairo, atk, gobject',
                  }
              },


)