import requests
from bs4 import BeautifulSoup
from glob import glob

# page = requests.get('https://nsc-db.github.io/units/')
# soup = BeautifulSoup('database.html', 'html.parser')

# links = []
# for i in soup.find_all('img'):
#     link = i.attrs['src']
#     print(link)
#     links.append('https://nsc-db.github.io/' + link)

paths = glob('database_files/*.png', recursive=True)
links = []
for i in paths:
    link = i.replace('database_files\\', 'https://nsc-db.github.io')
    links.append(link)




for link in links[:30]:
    link = link.replace('icons/thumb_', '').replace('7.png', '6.png')


    filename = link.split("/")[-1]

    r = requests.get(link, stream = True)
    with open(f'assets/cards/{filename}', 'wb') as f:
        f.write(r.content)
