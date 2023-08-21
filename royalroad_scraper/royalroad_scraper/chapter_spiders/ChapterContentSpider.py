import scrapy
import json
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



class ChapterContentSpider(scrapy.Spider):
    name = "chapter_content"

    # Get the path to the parent directory of the script
    script_dir = Path(__file__).resolve().parent
    
    # Construct the path to the output.json file
    output_json_path = script_dir.parent.parent / 'royalroad_scraper' / 'story_spiders' / 'output.json'

    # Read the URLs from the output.json file
    with open(output_json_path, 'r') as json_file:
        data = json.load(json_file)
        start_urls = [f"https://www.royalroad.com{item['first_chapter']}" for item in data]

    def parse(self, response):
        # Extract the story ID from the start URL
        story_id = response.url.split('/fiction/')[1].split('/')[0]

        # Extract chapter content
        chapter_content = response.css('.chapter-content').get()
        # Or use text() to extract only the text content without HTML tags
        # chapter_content = response.css('.chapter-content::text').get()

        yield {
            'story_id': story_id,
            'chapter_content': chapter_content,
        }

# Clear chapter_content.json before running
open("chapter_content.json", "w").close()
