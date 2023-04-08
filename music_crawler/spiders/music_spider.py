import os
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from scrapy import FormRequest, Request, Spider
from scrapy.exceptions import CloseSpider

from utils import convert_accented_vietnamese_text

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

EXCLUDE_KEYWORDS = [
    'edm','remix','version','ver','cover','intro',
    'beat','lien-khuc','mix','live','auto-tune',
    'lofi','karaoke', 'nonstop'
]

def load_authors():
    names = []
    with open('authors_vip.txt','r', encoding='utf-8') as f:
        for name in f.readlines():
            name = name.strip()
            names.append(name.lower())
    return names

def check_valid_author(author: str, valid_names: list):
    author_split = author.split(',')
    if len(author_split) == 1:
        author_split = author.split(';')
    if len(author_split) == 1:
        author_split = author.split('-')
    if len(author_split) == 1:
        author_split = author.split('/')
    if len(author_split) == 1:
        if author_split[0].lower() in valid_names:
            return True
    else: return False

def check_enough_data(table_file_dir, author):
    df = pd.read_csv(table_file_dir)
    count_value = (df['author'] == author).sum()
    if count_value >= 50:
        return True
    return False

def check_exist_data(table_file_dir, name):
    df = pd.read_csv(table_file_dir)
    df = df[df['name'] == name]
    if df.shape[0] == 0:
        return False
    return True

def clean_table(table_file_dir):
    df = pd.read_csv(table_file_dir,sep=',')
    old_shape = df.shape

    df = df.drop_duplicates(ignore_index=True)
    new_shape = df.shape
    df.to_csv(table_file_dir,sep=',',header=['author','name','lyric','audio_path','crawl_date'],index=False)
    if old_shape != new_shape:
        return True
    else:
        return False

class MusicSpiderSpider(Spider):
    name = 'music_spider'
    allowed_domains = ['chiasenhac.com']
    usn = 'nampham'
    psw = 'chiasenhac'
    pages = 20
    handle_httpstatus_list = [405]
    audio_dir = 'data/audios'
    table_file_dir = 'crawl_data.csv'
    custom_settings = {
        "CONCURRENT_REQUESTS": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
        # "CONCURRENT_REQUESTS_PER_IP": 3,
        "DOWNLOAD_DELAY": 1,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }
    if not os.path.exists('data'):
        os.mkdir('data')

    if not os.path.exists(audio_dir):
        os.mkdir(audio_dir)
    
    if not os.path.exists(table_file_dir):
        with open(table_file_dir, 'w+') as f_table:
            f_table.write('author,name,lyric,audio_path,crawl_date\n')

    # def start_requests(self):
    #     home_url = 'https://chiasenhac.vn/'
    #     yield Request(
    #         url=home_url,
    #         headers=HEADERS,
    #         callback=self.start_login
    #     )
    def start_requests(self):
        login_url = 'https://chiasenhac.vn/'
        yield FormRequest(
            url=login_url,
            formdata={'email': self.usn, 'password': self.psw},
            dont_filter=True,
            headers=HEADERS,
            callback=self.start_search_page
        )
        
    def start_search_page(self, response):
        # self.log(f"CODE {response.status}")
        headers = response.headers
        authors = load_authors()
        self.authors = authors
        for author in authors:
            for page in range(self.pages):
                self.log(f'CRAWLS MUSIC FROM AUTHOR: {author} ---- PAGE: {page + 1}')
                begin_url = 'https://chiasenhac.vn/tim-kiem?q='
                tail_url = f'&page_music={page + 1}&filter=sang-tac'
                url = begin_url + author + tail_url
                yield Request(
                    url=url,
                    dont_filter=True,
                    callback=self.parse_search_page,
                    headers=headers
                )

    def parse_search_page(self, response):
        # if check_enough_data(self.table_file_dir):
        #     CloseSpider("NUMBER OF DATA REACHED!!!!")

        if response.status != 200:
            yield {
                'status_code': response.status,
                'message': response.text,
                'url': response.url
            }
        else:
            headers = response.headers
            self.log(f'REQUEST {response.url} SUCCESSFULLY!!')
            href_xpath = '//p[@class="media-title mt-0 mb-0"]/a[@class="search_title"]/@href'
            song_items = response.xpath(href_xpath).getall()
            for index, url in enumerate(song_items):
                self.log(f'URL number: {index} ---- LINKS: {url}')
                if any([i in url for i in EXCLUDE_KEYWORDS]):
                    self.log('DETECTED EXLCLUDE KEYWORD')
                else:
                    self.log('START RETRIEVE DATA!!!')
                    yield Request(
                        url=url,
                        callback=self.parse_data,
                        dont_filter=True,
                        headers=headers
                    )

    def parse_data(self, response):
        # soup = BeautifulSoup(response.text, 'html.parser')
        name_xpath = '/html/body/section/div[3]/div/div[1]/div[3]/div[1]/div/div[2]/h2/text()'
        # download_xpath = soup.find_all('a','download_item')
        author_xpath = '/html/body/section/div[3]/div/div[1]/div[3]/div[1]/div/div[2]/ul/li[2]/a/text()'
        lyric_xpath = '//div[@id="fulllyric"]/text()'
        download_xpath = '//*[@id="pills-download"]/div/div[2]/div/div[1]/ul/li[1]/a/@href'

        name = response.xpath(name_xpath).get()
        author = response.xpath(author_xpath).get()
        lyric = response.xpath(lyric_xpath).getall()
        download_link = response.xpath(download_xpath).get()

        self.log(f'NAME: {name}')
        self.log(f'AUTHOR: {author}')
        self.log(f'LYRIC:\n {lyric}')
        self.log(f'DOWNLOAD LINK: {download_link}')

        if not check_valid_author(author, self.authors):
            self.log('INVALID AUTHOR --> STOP DOWNLOAD')
        else:
            data = {
                'name': name,
                'author':author,
                'lyric': lyric,
                'link': download_link
            }
            try:
                yield Request(
                    url=download_link,
                    callback=self.process_data,
                    headers=HEADERS,
                    cb_kwargs=dict(data=data)
                )
            except:
                raise Exception(f'DOWNLOAD {download_link} FAILED!!!')

    def process_data(self, response, data):
        self.log(f"DOWNLOAD SONG {data['link']} SUCCESSFULLY!!!")

        file_name = data['link'].split('/')[-1].replace('.html','')
        self.log(f'NAME EXTRACTED: {file_name}')

        # lyric_path = self.lyric_dir + '/' + name + '.txt'
        audio_path = self.audio_dir + '/' + file_name
        name = data['name'].lower().replace(',','')
        author = data['author'].lower()
        today = datetime.now().date()

        lyrics = []
        for line in data['lyric']:
            line = line.strip().lower()
            line = line.replace(',','')
            # line = convert_accented_vietnamese_text(line) // để có dấu nhét vào model, preprocess sẽ tính sau
            if line != '':
                lyrics.append(line)
        lyric = ' '.join(lyrics)
        # with open(lyric_path, 'w+') as f_lyric:
        #     f_lyric.write(' '.join(lyrics))
        if check_exist_data(self.table_file_dir, name):
            self.log('SONG EXISTED --> STOP SAVING')
        elif check_enough_data(self.table_file_dir, author):
            self.log(f'{author} REACHS LIMIT DATA --> STOP DOWNLOAD')
        elif lyric and response.body:
            with open(audio_path, 'wb+') as f_song:
                f_song.write(response.body)

            with open(f'{self.table_file_dir}','a+', encoding='utf-8') as f_table:
                f_table.write(f'{author},{name},{lyric},{audio_path},{today}\n')
        
            res = clean_table(self.table_file_dir)
            if res:
                self.log(f'CLEAN RESULT: {res}')
            else:
                self.log(f'NOTHING CHANGE')
