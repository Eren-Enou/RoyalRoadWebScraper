# scrapy runspider RoyalRoadRisingStarsTraversalSpider.py -o output.json


import scrapy
import os
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class RoyalRoadRisingStarsTraversalSpider(scrapy.Spider):
    name = "royalroadtraversal"
    start_urls = ['https://www.royalroad.com/fictions/rising-stars']

    def __init__(self, *args, **kwargs):
        super(RoyalRoadRisingStarsTraversalSpider, self).__init__(*args, **kwargs)

        # Initialize an empty list to store scraped data
        self.scraped_data = []

    def parse(self, response):
        # Extract the story items
        story_items = response.css('.fiction-list .fiction-list-item')

        for item in story_items:
            # Extract story title and its link and image
            img_url = item.css('img::attr(src)').get()
            title = item.css('.fiction-title a::text').get()
            story_link = item.css('.fiction-title a::attr(href)').get()

            # Extract the ID from the first chapter link
            story_id = story_link.split('/')[-2]

            # Construct the full URL for the story page
            full_story_link = response.urljoin(story_link)

            # Follow the link to the story page
            yield scrapy.Request(url=full_story_link, callback=self.parse_story_page, meta={
                'title': title,
                'img_url': img_url,
                'story_id': story_id
            })

    def parse_story_page(self, response):
        # Extract the title from the meta data
        title = response.meta['title']
        # Extract the image URL from the meta data
        img_url = response.meta['img_url']
        # Extract the first chapter ID from the meta data
        story_id = response.meta['story_id']
        # Extract the first chapter from the fic button in the header
        first_chapter = response.css('.fic-buttons a::attr(href)').get()
        # Extract the statistics numbers
        statistics_numbers = response.css('.list-unstyled .font-red-sunglo::text').getall()

        # Ensure we have at least 6 statistics numbers
        if len(statistics_numbers) < 6:
            return

        view_count, average_views, followers, favorites, ratings, pages = statistics_numbers[:6]

        scraped_data = {
            'title': title,
            'view_count': view_count,
            'average_views': average_views,
            'followers': followers,
            'favorites': favorites,
            'ratings': ratings,
            'pages': pages,
            'first_chapter': first_chapter,
            'img_url': img_url,
            'story_id': story_id
        }

        # Append the scraped data to the list
        self.scraped_data.append(scraped_data)

    def closed(self, reason):
        # Save the scraped data to a JSON file when the spider is closed
        output_file_path = "output.json"
        with open(output_file_path, 'w') as output_file:
            output_file.write('')  # Clear the file
            json.dump(self.scraped_data, output_file, indent=4)