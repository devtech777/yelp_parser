# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import html


class YelpItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(html.unescape), output_processor=TakeFirst()
    )
    item_url = scrapy.Field(output_processor=TakeFirst())
    biz_id = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field(output_processor=TakeFirst())
    phone = scrapy.Field(output_processor=TakeFirst())
    email = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(
        input_processor=MapCompose(html.unescape), output_processor=TakeFirst()
    )
    rating_value = scrapy.Field(output_processor=TakeFirst())
    review_count = scrapy.Field(output_processor=TakeFirst())
    categories = scrapy.Field(input_processor=MapCompose(html.unescape))
    home_url = scrapy.Field(output_processor=TakeFirst())
    hours = scrapy.Field()
    about = scrapy.Field(
        input_processor=MapCompose(html.unescape), output_processor=TakeFirst()
    )
    amenities = scrapy.Field(input_processor=MapCompose(html.unescape))
