import os
import json
import subprocess
from flask import Flask, render_template
from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from royalroad_scraper.royalroad_scraper.story_spiders.RoyalRoadRisingStarsTraversalSpider import RoyalRoadRisingStarsTraversalSpider
from royalroad_scraper.royalroad_scraper.chapter_spiders.ChapterContentSpider import ChapterContentSpider


app = Flask(__name__)

# Set the Twisted reactor to run in the main thread
os.environ['TWISTED_REACTOR'] = 'twisted.internet.selectreactor.SelectReactor'


# Define the paths to your JSON files
output_json_path = "output.json"
chapter_content_json_path = "chapter_content.json"

# Get the absolute path to the 'output.json' file
json_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'royalroad_scraper', 'royalroad_scraper', 'story_spiders', 'output.json'
)

# Get the path to the directory of the script
chapter_content_json_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'royalroad_scraper', 'royalroad_scraper', 'chapter_spiders', 'chapter_content.json'
)
# Load the data from the 'output.json' file
with open(json_file_path) as json_file:
    data = json.load(json_file)

# Organize data for sorting
stories = []
for item in data:
    story = {
        'title': item['title'],
        'follower_count': item['followers'],
        'view_count': item['view_count'],
        'pages': item['pages'],
        'image_url': item['img_url'],
        'first_chapter': item['first_chapter'],
        'story_id': item['story_id']
    }
    stories.append(story)
    
@app.route('/')
def index():
    # Clear the output.json and chapter_content.json files
    clear_json_files()

    # Run the spiders
    run_spiders()

    return render_template('index.html', stories=stories)


@app.route('/story/<int:story_id>')
def read_chapter(story_id):
    try:
        # Load chapter content from JSON file
        with open(chapter_content_json_path, 'r') as json_file:
            chapter_data = json.load(json_file)

        target_story_id = str(story_id)
        chapter_content = "test"  # Default value in case no matching item is found

        for item in chapter_data:
            if item["story_id"] == target_story_id:
                chapter_content = item["chapter_content"]
                break

        print(chapter_content)

        return render_template('readChapter.html', chapter_content=chapter_content, story_id=story_id)

    
    except Exception as e:
        # Handle exceptions here, e.g., return an error page
        print(e)
        return render_template('error.html', error_message=str(e))

    except FileNotFoundError:
        return "Chapter content JSON file not found."


def clear_json_files():
    if os.path.exists(output_json_path):
        os.remove(output_json_path)
    if os.path.exists(chapter_content_json_path):
        os.remove(chapter_content_json_path)


def run_spiders():
    subprocess.run(["python", "run_royal_road_spider.py"])
    subprocess.run(["python", "run_chapter_content_spider.py"])


if __name__ == '__main__':
    app.run(debug=True, port=3001)
