import scrapy
from scrapy.loader import ItemLoader

import json
import re
import html

from yelp.items import YelpItem


class BizSpider(scrapy.Spider):
    name = "biz"
    allowed_domains = ["www.yelp.com"]

    def start_requests(self):
        url = getattr(self, "biz", None)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        meta_bizid = response.xpath(
            '/html/head/meta[@name="yelp-biz-id"]/@content'
        ).get()
        data_content = response.xpath(
            '//script[@type="application/ld+json"]//text()'
        ).getall()
        data_json = response.xpath(
            '//script[@type="application/json"]//text()'
        ).getall()

        general_data = json.loads(data_content[0])
        business_data1 = self._prepare_json(data_json[2])
        business_data2 = self._prepare_json(data_json[3])
        biz_details1 = json.loads(business_data1)["bizDetailsPageProps"]
        biz_details2 = json.loads(business_data2)

        l = ItemLoader(item=YelpItem(), response=response)
        l.add_value("name", general_data["name"])
        l.add_value("item_url", response.url)
        l.add_value("biz_id", meta_bizid)
        l.add_xpath("image", '/html/head/meta[@property="og:image"]/@content')
        l.add_value(
            "phone",
            (general_data["telephone"] if "telephone" in general_data.keys() else None),
        )
        l.add_value(
            "email", (general_data["email"] if "email" in general_data.keys() else None)
        )
        l.add_value("address", general_data["address"])
        l.add_value("rating_value", general_data["aggregateRating"]["ratingValue"])
        l.add_value("review_count", general_data["aggregateRating"]["reviewCount"])
        l.add_value("categories", self._get_categories(data=data_content))
        l.add_value("home_url", self._get_homeurl(data=biz_details1))
        encid = "{'encid':'" + meta_bizid + "'}"
        client_platform = "{'clientPlatform':'WWW'}"
        l.add_value("hours", self._get_hours(encid=encid, data=biz_details2))
        l.add_value("about", self._get_about(data=biz_details1))
        l.add_value(
            "amenities",
            self._get_amenities(
                encid=encid, client_platform=client_platform, data=biz_details2
            ),
        )
        return l.load_item()

    def _prepare_json(self, json_data):
        # Uncomment
        json_data = re.sub("(<!--|-->)", "", json_data)
        # Correct quotes
        json_data = json_data.replace("\\&quot;", "'")
        # Unescape
        json_data = html.unescape(json_data)
        return json_data

    def _get_hours(self, encid, data):
        hours = []
        for i in range(7):
            key = f"$ROOT_QUERY.business({encid}).operationHours.regularHoursMergedWithSpecialHoursForCurrentWeek.{i}"
            if key in data.keys():
                day_of_week = data[key]["dayOfWeekShort"]
                hours.append({day_of_week: data[key]["hours"]["json"][0]})

        return hours

    def _get_amenities(self, encid, client_platform, data):
        amenities = []
        for i in range(30):
            try:
                key = f"$ROOT_QUERY.business({encid}).organizedProperties({client_platform}).0.properties.{i}"
                if data[key]["isActive"]:
                    amenities.append(data[key]["displayText"])
            except Exception:
                break

        return amenities

    def _get_homeurl(self, data):
        biz_contact_info = data["bizContactInfoProps"]
        if (
            biz_contact_info["businessWebsite"]
            and "linkText" in biz_contact_info["businessWebsite"].keys()
        ):
            home_url = biz_contact_info["businessWebsite"]["linkText"]
        else:
            home_url = None

        return home_url

    def _get_about(self, data):
        # Get Specialties and History
        try:
            biz_content_props = data["fromTheBusinessProps"][
                "fromTheBusinessContentProps"
            ]
            about = (
                biz_content_props["specialtiesText"]
                + "\n Established in "
                + biz_content_props["yearEstablished"]
                + "\n "
                + biz_content_props["historyText"]
            )
        except Exception:
            about = None

        return about

    def _get_categories(self, data):
        categories = []
        for i in range(1, len(data)):
            additional_data = json.loads(data[i])
            categories.append(additional_data["itemListElement"][-1]["item"]["name"])

        return categories
