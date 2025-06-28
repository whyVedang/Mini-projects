from pathlib import Path
from shutil import move
from os import rename
from organizer.rules import EXTENSION_MAP, KEYWORD_MAP
from os.path import exists,splitext,join,basename

def exist(path:Path):
    if not exists(path):
        path.mkdir(parents=True,exist_ok=True)

def movef(file,destination):
    exist(destination)
    filename=basename(file)
    new=join(destination,filename)
    if exists(new):
        Newname,ext=splitext(filename)
        c=1
        while exists(join(destination,f'{Newname}{str({c})}{ext}')):
            newName=f'{filename} ({str(c)}){ext}'
            c+=1
        filenew=f'{Newname}{str({c})}{ext}'
        new=join(destination,filenew)
    move(file,destination)
    print(f'Moved {file} to => {destination}')


def createf(file):
    pass

def category(file):
    pass

def subcategory(file,main):
    pass