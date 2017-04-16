 #!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
ZULULAND / DEBUG :: rev_24 :: JUN2014 :: msarch@free.fr
global vars and constants

"""
##---IMPORTS ------------------------------------------------------------------
import inspect

##---VARIABLES-----------------------------------------------------------------
DEBUG=0

##---DEBUG PRINT-----------------------------------------------------------------
def db_print(*msgs):
    if DEBUG:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        print 'debug msg from [',mod.__name__,'/',calframe[1][3],'] -->',
        #print 'debug msg from [',mod,'/',calframe[1][3],'] -->',
        for msg in msgs:
            print msg,
        print ''
        # TODO : formater le print proprement sur le mode :
        # print '[%s] %s' % (mod.__name__, msg)
    else:
        pass

