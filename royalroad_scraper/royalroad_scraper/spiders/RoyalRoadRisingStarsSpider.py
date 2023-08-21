import scrapy

class RoyalRoadRisingStarsSpider(scrapy.Spider):
    name = "royalroad"
    start_urls = ['https://www.royalroad.com/fictions/rising-stars']

    def parse(self, response):
        # Extract the story titles, data, and image URLs
        story_titles = response.css('.fiction-title a::text').getall()
        story_data = response.css('.stats .col-sm-6 span::text').getall()
        story_images = response.css('.fiction-list-item img.img-responsive::attr(src)').getall()

        print("Number of titles:", len(story_titles))
        print("Number of data elements:", len(story_data))
        print("Number of img elements:", len(story_images))

        # Each title has 4 data elements: follower_count, view_count, rating, chapters
        data_per_title = 4
        num_titles = len(story_titles)
        
        # Ensure the number of titles and images match
        if num_titles != len(story_images):
            print("Number of titles and images don't match")
            return
        
        for i in range(0, num_titles * data_per_title, data_per_title):
            title = story_titles[i // data_per_title]
            follower_count = story_data[i]
            page_count = story_data[i + 1]
            view_count = story_data[i + 2]
            chapters = story_data[i + 3]
            image_url = story_images[i // data_per_title]
            
            yield {
                'title': title,
                'follower_count': follower_count,
                'page_count': page_count,
                'view_count': view_count,
                'chapters': chapters,
                'image_url': image_url
            }


        # Follow pagination links if available
        # next_page = response.css('.pagination .next a::attr(href)').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)
