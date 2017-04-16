# creating a dictionary from a text file
# key value pairs occupy a line and are separated by a space

# data for the test file of name bowling_score pairs
text = """\
Frank 180
Larry 215
Heidi 150"""

fname = "Bowling.txt"
# write the test file
fout = open(fname, "w")
fout.write(text)
fout.close()

# read the test file in and convert to a dictionary
bowling_dict = {}
for line in open(fname):
    name, score = line.split()
    bowling_dict[name] = int(score)

print( bowling_dict )  # {'Frank': 180, 'Larry': 215, 'Heidi': 150}
