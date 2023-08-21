import scrapy

class RoyalRoadRisingStarsSpider(scrapy.Spider):
    name = "royalroad"
    start_urls = ['https://www.royalroad.com/fictions/rising-stars']

    def parse(self, response):
    # Extract the story items
        story_items = response.css('.fiction-list .fiction-list-item')

        for item in story_items:
            # Extract story title and its link and image
            img_url = item.css('img::attr(src)').get()
            print(img_url)
            title = item.css('.fiction-title a::text').get()
            story_link = item.css('.fiction-title a::attr(href)').get()

            # Construct the full URL for the story page
            full_story_link = response.urljoin(story_link)

            # Follow the link to the story page
            yield scrapy.Request(url=full_story_link, callback=self.parse_story_page, meta={'title': title, 'img_url': img_url})

    def parse_story_page(self, response):
        # Extract the title from the meta data
        title = response.meta['title']
        # Extract the image URL from the meta data
        img_url = response.meta['img_url']
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

        yield {
            'title': title,
            'view_count': view_count,
            'average_views': average_views,
            'followers': followers,
            'favorites': favorites,
            'ratings': ratings,
            'pages': pages,
            'first_chapter': first_chapter,
            'img_url': img_url
        }
