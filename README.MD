# Yelp Parser
Yelp parser built with Python 3.6+ and Scrapy. 
Scrape Yelp for restaurants, bars, gyms etc.

Installation:
-------------
```
    $ git clone https://github.com/devtech777/yelp_parser
    $ cd yelp_parser
    $ pip install -r requirements.txt
```

Usage:
-------------
Example usage for scraping Yelp.

To get info about [this](https://www.yelp.com/biz/cracked-and-battered-marina-san-francisco) restaurant use parameter "-a biz={url to business}" and save it to "result.json" file:
```
scrapy crawl biz -O result.json -a biz=https://www.yelp.com/biz/cracked-and-battered-marina-san-francisco
```

Results:
-------------
You can check JSON examples in "result_examples" folder.
