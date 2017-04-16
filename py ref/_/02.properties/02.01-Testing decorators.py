
##--- SimplePoint--------------------------------------------------------------
class Foo(object):

    def __init__(self):
        self._val = 3

    @property
    def val(self):          # access through decorator
        return self._val
    
    @val.setter
    def val(self,n):
        self._val=n
   
    def val2(self):
        return self._val+100

    @property
    def val3(self):
        return self._val+200
    
    @val3.setter
    def val3(self,n):
        # it is not possible to set p.val3 !!!!
        # recursive definition will occur
        self.val3=n
    

def main():
    
    p =Foo()
    
    print 'p._val is 3'
    print 'accessing \'val\'through decorator\t\t --> %d' % p.val
    print 'accessing the private attribute \'_val\'\t\t --> %d' % p._val
    print 'printing result of function \'val2()\'\t\t --> %d' % p.val2()
    print 'accessing \'val3\'through decorator\t\t --> %d' % p.val3
    print '\n----------------\n'
    
    p._val = 5
    
    print 'changed p._val to 5'
    print 'accessing \'val\'through decorator\t\t --> %d' % p.val
    print 'accessing the private attribute \'_val\'\t\t --> %d' % p._val
    print 'printing result of function \'val2()\'\t\t --> %d' % p.val2()
    print 'accessing \'val3\'through decorator\t\t --> %d' % p.val3
    print '\n----------------\n'

    p.val = 7

    print 'changed p.val to 7'
    print 'accessing \'val\'through decorator\t\t --> %d' % p.val
    print 'accessing the private attribute \'_val\'\t\t --> %d' % p._val
    print 'printing result of function \'val2()\'\t\t --> %d' % p.val2()
    print 'accessing \'val3\'through decorator\t\t --> %d' % p.val3
    print '\n----------------\n'
    
    # p.val3 = 123456 # raises an error
    p.val2 = 123
    print p.val2
    print p.val2()
    
if __name__ == "__main__": main()