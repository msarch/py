#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Les propriétés apparaissent pour l'utilisateur de la classe comme de simples
#attributs de classe publics mais elles sont en fait des attributs privés
#uniquement accessibles par des accesseurs.

#Pour mieux comprendre nous allons utiliser une classe convertisseur.
#Cette classe dispose de deux propriétés : euros et francs.
#Nous souhaitons que la valeur stockée dans euros soit toujours cohérente
#avec celle de francs, et vis-versa. Pour ce faire nous allons utiliser
#les propriétés.

#Comme je l'ai indiqué plus haut, les propriétés sont en fait un ensemble
#attributs privés/accesseurs. Il faut donc commencer par déclarer nos deux
#attributs privés puis les méthodes de classe qui vont gérer leurs valeurs.
#Ensuite la fonction property va nous permettre de créer la propriété
#correspondante :class convertisseur(object):

def __init__(self):
    self.__taux = 6.55957
    self.__euros = 0
    self.__francs = 0

# accesseurs en lecture
def getEuros(self):
    return self.__euros

def getFrancs(self):
    return self.__francs

# accesseurs en écriture
def setEuros(self, euros):
    self.__euros = euros
    self.__francs = self.__euros*self.__taux

def setFrancs(self, francs):
    self.__francs = francs
    self.__euros = self.__francs/self.__taux

# declaration des propriétés
euros = property(getEuros, setEuros)
francs = property(getFrancs, setFrancs)

if __name__ == '__main__':
    test = convertisseur()

    test.francs = 10
    print('%.2f francs -> %.2f euros' %(test.francs, test.euros))

    test.euros = 25
    print('%.2f francs -> %.2f euros' %(test.francs, test.euros))
