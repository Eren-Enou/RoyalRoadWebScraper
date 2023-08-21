import scrapy
import json

class ChapterContentSpider(scrapy.Spider):
    name = "chapter_content"

    # Read the URLs from the output.json file
    with open('output.json', 'r') as json_file:
        data = json.load(json_file)
        start_urls = [f"https://www.royalroad.com{item['first_chapter']}" for item in data]

    def parse(self, response):
        # Extract chapter title
        chapter_title = response.css('.chapter-title::text').get()

        # Extract chapter content
        chapter_content = response.css('.chapter-content').get()
        # Or use text() to extract only the text content without HTML tags
        # chapter_content = response.css('.chapter-content::text').get()

        yield {
            'chapter_title': chapter_title,
            'chapter_content': chapter_content,
        }
