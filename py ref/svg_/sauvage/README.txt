sauvage is a python library that displays svg graphics with opengl for
interaction purpose.
http://www.tls.cena.fr/~conversy/research/sauvage
it's a derived work from svgl (http://svgl.sf.net)

copyright (c) 2005-2007 stephane conversy
stepahne ___dot___ conversy ____at___ enac.fr

licence: LGPL (see gnu.org, and the LICENSE file)

what's new: see at the end of this file

-------------------------

build:
you'll need:
# should already be there on linux, with fink or darwinport on macosx
# glib                  http://www.gtk.org/download/
# pango                 http://www.gtk.org/download/
# freetype              http://www.freetype.org/
# fontconfig            http://www.fontconfig.org/wiki/

# should already be there if you do python dev
# (on macosx, see http://undefined.org/python/#pimp and http://pythonmac.org/packages/)
# wxPython              http://www.wxpython.org/
# numpy      http://numpy.scipy.org/
# PIL
# opengl-ctypes (formely pyopengl):
#	install easy_install (d/l http://peak.telecommunity.com/dist/ez_setup.py and run it)
#	type "easy_install -U PyOpenGL" in a shell

# SWIG                  http://www.swig.org/
#	swig is not mandatory as I included the _wrap files. It's only needed if you plan to tweak extensions
#	on MacOSX, the fink version does not work, install a fresher version

# easy to get/compile/install
# Anti-Grain Geometry   2.4        http://www.antigrain.com/
# since agg is not widespread, I decided to include agg sources in sauvage sources, see src/agg-2.4/readme and src/agg-2.4/copying
# the following is obsolete:
#	on MacOSX, you may experience failure due to freetype
#	instead of installing the fink version of freetype, after configure just do:
#		cd src && make install-exec
#		cd include && make install-data

on mandriva:
# urmpi lib64pango1.0_0-devel lib64python2.4-devel lib64Mesaglut3-devel lib64wxPythonGTK2.6 python-numeric python-imaging


to build it on a unix-like machine:

% cd /where/you/want/to/put/it
% tar xvjf sauvage.tbz
% cd sauvage
% make

you can build it in a separate dir (ala gcc):
% mkdir ../build/sauvage
% cd ../build/sauvage
% ln -s ../../src/sauvage/Makefile .
% ln -s ../../src/sauvage/data .
% make

if it doesn't compile, edit Makefile to reflect various path.
feel free to send any comments to stephane ____dot___ conversy ___at___ enac.fr

testing it:

% make draw
% make tut-00 tut-01 tut-02
% make test

-------------------------------

what's new

0.3.3:
updated to python2.5 and opengl-ctypes
addded agg-2.4 sources to ease building

0.3.2:
make it work with shaders
try 'make kabuki'

wrote a simple draw and a new Tk-like API:
try 'make draw'
more apps/draw/main.py

0.3.1:
more svg compliance

0.3:
new stuff

0.2:
initial release


