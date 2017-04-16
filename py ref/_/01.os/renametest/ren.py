# Python renamer script: creates a function called pyrename(). pyrename() will rename all files in a given folder.
# Usage: Put all the files you want to rename in an isolated folder. The function can be called by typing pyrename().
# Warning, this script will rename your files. There is no undo. Use with care. 
def pyrename():
    'Put all the files you want to rename in an isolated folder. The function can be called by typing pyrename().'
    import os

    #function to ignore the hidden . files in a directory. Note the use of the 'yield' keyword
    def listdir_nohidden(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                yield f
                
    path = raw_input('path to folder?: ')
    #get the files from the folder and put the filenames in a list called files
    theFiles  = listdir_nohidden(path)
    files = []
    for f in theFiles:
        files.append(f)

    #user supplied values
    print 'Want to replace a character or string in your file names?'
    want_to_replace = raw_input('Type y or n. Or to completely rename type w: ')
    if want_to_replace == 'y':
        replace = raw_input('Type the character or string that you want to replace (FYI can be a space!): ')
        replace_with = raw_input('Type the character or string that you want to replace with: ')
    elif want_to_replace == 'w':
        replace = ''
        replace_with = raw_input('Type new name: ')
    else:
        replace = ''
        replace_with = ''   

    if want_to_replace != 'w':
        want_numbers = raw_input('Want your files numbered? type y or n: ')
        if want_numbers == 'y':
            zeros = raw_input('Type the amount of padding zeros you need (using a single integer, like 4): ')
        else:
            zeros = 0

    if want_to_replace == 'w':
        zeros = raw_input('Type the amount of padding zeros you need (using a single integer, like "4"): ')

    ext = raw_input('Please type the three letter extension you want to use ex: jpg (NOT the .): ')
    

    #remove extension, put the filenames in a list called names
    names = []
    for f in files:
        if f[-4] == '.':
            names.append(f.replace(f[-4:], ''))
        else:
            names.append(f)

    #add new names, add user supplied extension, put the filenames in a list called namesPlusEx
    namesPlusEx = []
    count = 0
    for f in names:
        if want_to_replace == 'w':
            namesPlusEx.append(f.replace(f, replace_with)+ (('.%.')+zeros+('d'))% count +'.'+ ext) 
        elif want_to_replace != 'w' and want_numbers == 'y':
            namesPlusEx.append(f.replace(replace, replace_with)+ (('.%.')+zeros+('d'))% count +'.'+ ext)
        else:
            namesPlusEx.append(f.replace(replace, replace_with)+'.'+ ext)
        count += 1

    #rename the actual files
    c=0
    for f in files:
        os.rename(path+'/'+f, path+'/'+namesPlusEx[c])
        c+=1

    print 'You have re-named %d files' % len(files)
