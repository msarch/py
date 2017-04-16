#!/usr/bin/env python

import string,glob
import os

print "debut"
os.chdir("/disk_catia/TRANSFERT/HPGL")  # se positionne dans le repertoire de traitement

list_fic = glob.glob("*.hpgl")
list_fic.sort()
for fic_hpgl in list_fic:
    fic_dxf="%s.dxf" % fic_hpgl[:-5]
    print "%s traitement en cours ->" % fic_hpgl ,
    # test existance fichier dxf ou fichier hpgl plus recent
    if not os.path.exists(fic_dxf)\
    or os.path.getmtime(fic_dxf)<os.path.getmtime(fic_hpgl):
        r=open(fic_hpgl,"r")   # ouvre le fichier en lecture
        w=open(fic_dxf,"w")    # ouvre le fichier en ecriture
        liste=r.readlines()    # lit le fichier sous forme de ligne

        w.writelines(['  0\nSECTION\n  2\nENTITIES\n'])
        pt=0
        for i in liste:
            l_split=string.split(i[:-1],";")  # ligne -> liste (separateur ";")
                                                  # [:-1] enleve le dernier caractere
            for j in l_split:                 # de la ligne -> \012 (retour a la ligne)
                if j[0:2]=='PU':
                    pt_split=string.split(j[2:],",") # ligne -> (sep ',')
                    w.writelines(['  0\nLINE\n  8\n0\n'])
                    w.writelines([' 10\n',pt_split[0],'\n'])
                    w.writelines([' 20\n',pt_split[1],'\n'])
                if j[0:2]=='PD':
                    pt_split=string.split(j[2:],",")
                    w.writelines([' 11\n',pt_split[0],'\n'])
                    w.writelines([' 21\n',pt_split[1],'\n'])
            pt=pt+1
        if pt==1000:
            pt=0
        print ".",
        w.writelines(['  0\nENDSEC\n  0\nEOF\n'])

        r.close()
        w.close()
        print fic_dxf
    else:
        print "OK"
print "fin"

