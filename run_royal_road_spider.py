import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from royalroad_scraper.royalroad_scraper.story_spiders.RoyalRoadRisingStarsTraversalSpider import RoyalRoadRisingStarsTraversalSpider

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(RoyalRoadRisingStarsTraversalSpider)
process.start()
