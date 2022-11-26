import os, re
from scrapy import Request, Spider
from utils import convert_accented_vietnamese_text

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

EXCLUDE_KEYWORDS = [
    'edm','remix','version','ver','cover','intro',
    'beat','lien-khuc','mix','live','auto-tune'
]

def load_authors():
    urls = []
    with open('authors.txt','r', encoding='utf-8') as f:
        for url in f.readlines():
            urls.append(url.strip())
    return urls

class MusicSpiderSpider(Spider):
    name = 'music_spider'
    allowed_domains = ['chiasenhac.com']

    nb_pages = 1
    lyric_dir = 'lyrics'
    song_dir = 'songs'

    custom_settings = {
        "CONCURRENT_REQUESTS": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
        # "CONCURRENT_REQUESTS_PER_IP": 3,
        "DOWNLOAD_DELAY": 15,
        "RANDOMIZE_DOWNLOAD_DELAY": True
    }

    if not os.path.exists(lyric_dir):
        os.mkdir(lyric_dir)

    if not os.path.exists(song_dir):
        os.mkdir(song_dir)


    def start_requests(self):
        authors = load_authors()
        for author in authors:
            for page in range(self.nb_pages):
                self.log(f'CRAWLS MUSIC FROM AUTHOR: {author} ---- PAGE: {page + 1}')
                begin_url = 'https://chiasenhac.vn/tim-kiem?q='
                tail_url = f'&page_music={page + 1}&filter=sang-tac'
                url = begin_url + author + tail_url
                yield Request(
                    url=url,
                    callback=self.parse_search_page,
                    dont_filter=True,
                    headers=HEADERS
                )

    def parse_search_page(self, response):
        if response.status != 200:
            yield {
                'status_code': response.status,
                'message': response.text,
                'url': response.url
            }
        else:
            self.log(f'REQUEST {response.url} SUCCESSFULLY!!')
            href_xpath = '//p[@class="media-title mt-0 mb-0"]/a[@class="search_title"]/@href'
            song_items = response.xpath(href_xpath).getall()
            for index, url in enumerate(song_items):
                self.log(f'URL number: {index} ---- LINKS: {url}')
                if any([i in response.url for i in EXCLUDE_KEYWORDS]):
                    self.log(f'DETECTED EXLCLUDE KEYWORD')
                else:
                    yield Request(
                        url=url,
                        callback=self.parse_data,
                        dont_filter=True,
                        headers=HEADERS
                    )

    def parse_data(self, response):
        download_xpath = '//*[@id="pills-download"]/div/div[2]/div/div[1]/ul/li[1]/a/@href'
        author_xpath = '/html/body/section/div[3]/div/div[1]/div[3]/div[1]/div/div[2]/ul/li[2]/a/text()'
        lyric_xpath = '//div[@id="fulllyric"]/text()'

        author = response.xpath(author_xpath).get()
        download_link = response.xpath(download_xpath).get()
        lyric = response.xpath(lyric_xpath).getall()

        self.log(f'AUTHOR: {author}')
        self.log(f'LYRIC:\n {lyric}')
        self.log(f'DOWNLOAD LINK: {download_link}')

        data = {
            'link': response.url,
            'author':author,
            'lyric': lyric
        }

        try:
            yield Request(
                url=download_link,
                callback=self.process_data,
                dont_filter=True,
                headers=HEADERS,
                cb_kwargs=dict(data=data)
            )
        except:
            raise Exception(f'DOWNLOAD {download_link} FAILED!!!')

    def process_data(self, response, data):
        self.log(f"DOWNLOAD SONG {data['link']} SUCCESSFULLY!!!")

        name = data['link'].split('/')[-1].replace('.html','')
        self.log(f'NAME EXTACTED: {name}')

        lyric_path = self.lyric_dir + '/' + name + '.txt'
        song_path = self.song_dir + '/' + name + '.m4a'

        lyric = []
        for line in data['lyric']:
            line = line.strip()
            line = convert_accented_vietnamese_text(line)
            if line != '':
                lyric.append(line)

        with open(lyric_path, 'w+') as f_lyric:
            f_lyric.write(' '.join(lyric))
        
        with open(song_path, 'wb+') as f_song:
            f_song.write(response.body)
