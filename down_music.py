import requests
from bs4 import BeautifulSoup
from time import sleep
import re

###Phát hiện rằng trong link bài hát có slash/các-ca sĩ thể hiện/ nên có thể lọc số ca sĩ ở đây 'thử' để hạn chế lọc lúc sau

### Download nhạc từ link bài hát
# url = 'https://chiasenhac.vn/mp3/min/em-moi-la-nguoi-yeu-anh-tsvc00rdqvnnam.html'
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# link_down = soup.find_all('a','download_item')[0]['href']
# r2 = requests.get(link_down)
# with open('mp4.m4a', 'wb+') as f:
#     f.write(r2.content)
# for i in range(10):
#     print(i)

### Lấy link bài hát từ link nghệ sỹ
# url2= 'https://chiasenhac.vn/ca-si/den-zsswz637q91kwt.html?tab=music'
# r = requests.get(url2)
# soup = BeautifulSoup(r.text, 'html.parser')
# class_name = 'media-title mt-0 mb-0'
# a= soup.find_all('h5',class_name)
# hrefs = [i.next['href'] for i in a]

# for i in hrefs:
#     print(i)
#     r1 = requests.get(i)
#     soup = BeautifulSoup(r1.text, 'html.parser')
#     link_down = soup.find_all('a','download_item')[0]['href']
#     name = link_down.split('/')[-1]
#     try:
#         r2 = requests.get(link_down)
#         print(f'Tải {name} thành công')
#         with open(f'{name}.m4a', 'wb+') as f:
#             f.write(r2.content)
#     except:
#         raise Exception(f'Tải {name} thất bại')

# urll = 'https://chiasenhac.vn/mp3/den-nguyen-thao/mang-tien-ve-cho-me-tsv75b7qqthqte.html'
# r1 = requests.get(urll)
# soup = BeautifulSoup(r1.text, 'html.parser')
# link_down = soup.find_all('a', 'download_item')[1]['href']
# print(soup.find_all('a', 'download_item')[1])
# author_class = soup.find_all('span', string='Sáng tác: ')[0].nextSibling.text
# name = link_down.split('/')[-1]
# try:
#     r2 = requests.get(link_down)
# except:
#     print('Không được rồi bro!!')

# import pandas as pd
# df = pd.read_csv('crawl_data.csv',sep=',',names=['author','l_p','s_p','date'])
# # a = df.groupby(df.columns[0], observed=True).count()
# print(df.shape)
# # b = a.columns[0]
# print(df.drop_duplicates(ignore_index=True))

# EXCLUDE_KEYWORDS = [
#     'edm','remix','version','ver','cover','intro',
#     'beat','lien-khuc','mix','live','auto-tune'
# ]

# a = 'test tên;dsadsa'
# url = 'data/lyrics/love-rosie-cover)-tsv7ttvzqtff21.txt'
# b = [True, True, False, False]

# print(c)
# if any([i in url for i in EXCLUDE_KEYWORDS]):
#     print(f'DETECTED EXLCLUDE KEYWORD')
# else: print('Có cái cc')

home = 'https://chiasenhac.vn/'

r1 = requests.get(home)
soup = BeautifulSoup(r1.text, 'html.parser')
print(1)
print(2)