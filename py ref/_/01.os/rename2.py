import os


TARGET_DIR = '/home/User/files/tmp/'

for FILE_OLD in os.listdir(TARGET_DIR):

    FILE_NEW = FILE_OLD.replace(' ', '')
    FILE_NEW = FILE_NEW.upper()

    FILE_OLD = TARGET_DIR + FILE_OLD
    FILE_NEW = TARGET_DIR + FILE_NEW

    print 'Renaming', FILE_OLD, 'to', FILE_NEW
    os.rename(FILE_OLD, FILE_NEW)
