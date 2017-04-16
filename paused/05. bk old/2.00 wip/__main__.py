

#!/usr/bin/python
# -*- coding: utf-8 -*-

# msarch@free.fr * feb 2015 * bw-rev116

##--- IMPORTS -----------------------------------------------------------------
from bw.loader import get_folder, load_scene
from bw.pygloop import start

##--- MAIN --------------------------------------------------------------------
if __name__ == "__main__":
    print ':: bbw'
    f = get_folder()
    load_scene(f)
    start()