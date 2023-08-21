import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class RoyalRoadRisingStarsTraversalSpider(scrapy.Spider):
    name = "royalroadtraversal"
    start_urls = ['https://www.royalroad.com/fictions/rising-stars']
    
    def __init__(self, *args, **kwargs):
        super(RoyalRoadRisingStarsTraversalSpider, self).__init__(*args, **kwargs)

        # Clear and create a new output.json before running
        self.output_file_path = "output.json"
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)
        with open(self.output_file_path, 'w') as output_file:
            output_file.write('[]')  # Write an empty JSON array
        
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

        view_count = statistics_numbers[0]
        average_views = statistics_numbers[1]
        followers = statistics_numbers[2]
        favorites = statistics_numbers[3]
        ratings = statistics_numbers[4]
        pages = statistics_numbers[5]

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
        
        # Append the data to the output.json file
        with open(self.output_file_path, 'r+') as output_file:
            data = json.load(output_file)
            data.append(scraped_data)
            output_file.seek(0)
            json.dump(data, output_file, indent=4)
            output_file.truncate()

