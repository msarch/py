# this script d/l and installs various softwares needed to use sauvage
# it uses fink as much as possible, and compiles other packages when needed
# compiled packages are installed in /usr/local
# sudo is used to install stuff

# from fink faq
# Q5.10: I'm tired of typing my password into sudo again and again. Is there a way around this?
#A: If you're not paranoid, you can configure sudo to not ask you for a password. To do this, run visudo as root and add a line like this:
# username ALL = NOPASSWD: ALL
# Replace username with your actual username, of course. This line allows you to # run any command via sudo without typing your password.


# ----------------------------------------------------------
# packages from fink

sudo apt-get install expat gettext pkgconfig wget libtool

# ----------------------------------------------------------
# python stuff

wget http://undefined.org/python/MacPython-OSX-2.4.1-1.dmg
open MacPython-OSX-*.dmg
sudo installer -target / -pkg /Volumes/MacPython-OSX-*/*pkg

wget http://pythonmac.org/packages/TigerPython24Fix-r2.zip
unzip TigerPython24Fix-r2.zip
sudo installer -target / -pkg TigerPython24Fix*/*pkg

wget http://pythonmac.org/packages/Numeric-23.7-py2.4-macosx10.3.zip
unzip Numeric*zip
sudo installer -target / -pkg Numeric*/*pkg

wget http://pythonmac.org/packages/PIL-1.1.5-py2.4-macosx10.3.zip
unzip PIL*zip
sudo installer -target / -pkg PIL*/*pkg

wget http://pythonmac.org/packages/PyOpenGL-2.0.2.01-py2.4-macosx10.3.zip
unzip PyOpenGL*zip
sudo installer -target / -pkg PyOpenGL*/*pkg

#wget http://pythonmac.org/packages/wxPython-2.6_unicode-py2.4-macosx10.3.zip
#unzip wxPython*zip
wget http://heanet.dl.sourceforge.net/sourceforge/wxpython/wxPython2.6-osx-unicode-2.6.3.0-macosx10.3-py2.4.dmg
open wxPython*dmg
sudo installer -target / -pkg wxPython*/*pkg

# ----------------------------------------------------------
# packages not working from fink

export PATH=/usr/local/bin:$PATH

configure_cmd="env CPPFLAGS=-I/sw/include LDFLAGS=-L/sw/lib PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure"

wget -nc -c http://savannah.nongnu.org/download/freetype/freetype-2.1.10.tar.bz2
tar xvjf freetype*

(cd freetype*
$configure_cmd
make
sudo make install
)

wget -nc -c http://www.fontconfig.org/release/fontconfig-2.3.2.tar.gz
tar xvzf fontconfig*

(cd fontconfig*
$configure_cmd
make
sudo make install
)

wget -nc -c ftp://ftp.gtk.org/pub/gtk/v2.8/glib-2.8.3.tar.bz2
tar xvjf glib*

(cd glib*
$configure_cmd
make
sudo make install
)

wget -nc -c ftp://ftp.gtk.org/pub/gtk/v2.8/pango-1.10.1.tar.bz2
tar xvjf pango*

(cd pango*
$configure_cmd --without-x
make
sudo make install
)

wget -nc -c http://prdownloads.sourceforge.net/swig/swig-1.3.27.tar.gz
tar xvjf swig*

(cd swig*
$configure_cmd
make
sudo make install
)

wget -nc -c http://www.antigrain.com/agg23.tar.gz
tar xvzf agg*
(cd agg*
sh autogen.sh
cd src
g++ -I../include -c *.cpp
g++ -dynamiclib *.o -o libagg.dylib
cd ..
sudo mkdir /usr/local/include/agg2
sudo cp -R include/*
sudo cp src/libagg.dylib /usr/local/lib
sudo cp libagg.pc /usr/local/lib/pkgconfig
)

#echo "now you can type 'make' in the sauvage/ directory"

wget -nc -c http://www.tls.cena.fr/~conversy/research/sauvage/sauvage.tbz
tar xvjf sauvage.tbz

(cd sauvage*
make test
)

