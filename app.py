import os
import json

from flask import Flask, render_template

app = Flask(__name__)

# Get the absolute path to the 'output.json' file
json_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'royalroad_scraper', 'royalroad_scraper', 'spiders', 'output.json'
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
        'first_chapter': item['first_chapter']
    }
    stories.append(story)

@app.route('/')
def index():
    return render_template('index.html', stories=stories)

if __name__ == '__main__':
    app.run(debug=True, port=3001)
