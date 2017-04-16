
'''

	Project:	CS100
	Title:		Tools
	
	Author:		John Mooney
	Date:		06/28/2012

	Description:
		A set of handy-dandy tools for common python functionality 
'''

import math
twoPi = 2*math.pi
pi2 = math.pi/2


def nearEq(f1, f2, de=.000001):
	dif = abs(f2-f1)
	return dif <= de


def getValidIndex(prevIndex, increment, cap):
	nextIndex = prevIndex+increment
	if(nextIndex < 0 or nextIndex > cap-1):
		nextIndex = prevIndex

	return nextIndex

def getDictValue(dict, defaultValue, possibleValues, raiseError=False):
	for val in possibleValues:
		if(val in dict):
			return dict[val]
			
	if not raiseError:
		return defaultValue
	else:
		raise TypeError("Missing Necessary Keyword Argument: " + possibleValues[-1])
