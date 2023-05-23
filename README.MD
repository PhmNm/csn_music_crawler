# USAGE

1. Terminal should point to the folder that contains [scrapy.cfg](/music_crawler/scrapy.cfg)

2. Run this script to start crawl:

    ```terminal
    scrapy crawl music_spider
    ```

3. To change download delay (present: 5s with randomize) setting, go to [music_spider.py](/music_crawler/spiders/music_spider.py) and change the [custom_settings](/music_crawler/spiders/music_spider.py#L81-L82).

4. To change nb_pages of searching (present: 10), go to [music_spider.py](/music_crawler/spiders/music_spider.py) and change the [custom_settings](/music_crawler/spiders/music_spider.py#L73-L74).
