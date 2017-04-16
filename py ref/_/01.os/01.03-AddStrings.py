#!/usr/bin/python



str1 = "Hello"
str2 = "World"
newstr1 = "".join((str1, str2))
newstr2 = " ".join((str1, str2))
newstr3 = "blah".join((str1, str2))

print newstr1
print newstr2
print newstr3

# simple :

s  = 'foo'
s += 'bar'
s += 'baz'

print s

# or :

l = []
l.append('foo')
l.append('bar')
l.append('baz')

s = ''.join(l)

print s
