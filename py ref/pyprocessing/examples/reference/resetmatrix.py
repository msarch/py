from pyprocessing import *

noFill();
box(80);
printMatrix();
# Processing prints
# 01.0000  00.0000  00.0000 -50.0000
# 00.0000  01.0000  00.0000 -50.0000
# 00.0000  00.0000  01.0000 -86.6025
# 00.0000  00.0000  00.0000  01.0000

resetMatrix();
box(80);
printMatrix();
# Prints:
# 1.0000  0.0000  0.0000  0.0000
# 0.0000  1.0000  0.0000  0.0000
# 0.0000  0.0000  1.0000  0.0000
# 0.0000  0.0000  0.0000  1.0000

run()