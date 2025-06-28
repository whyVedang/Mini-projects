from pathlib import Path
from handler import category,subcategory,exist,movef
p = Path.home() / 'Downloads'
print(p)
t=Path.home() /'V:/DownloadSorter'
print(t)
def organizer():
    for file in p.iterdir():
        if file.is_file:
            main=category(file)
            sub=subcategory(file,main)
            target=t / 'main / sub'
            exist(target)
            movef(file,target)
