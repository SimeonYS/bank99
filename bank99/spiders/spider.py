import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import Bank99Item
from itemloaders.processors import TakeFirst
import w3lib.html
pattern = r'(\xa0)?(😁)?(👵)?(👴)?(💬)?(🔒)?'

class Bank99Spider(scrapy.Spider):
	name = 'bank99'
	start_urls = ['https://bank99.at/blog/']


	def parse(self, response):
		# get all categories, parse them one by one

		categories = response.xpath('//div[@class="jsx-3948985667 row"]//div[@class="jsx-1865412968 card-content "]//a[@class="jsx-1191953325 jsx-4098142206 font-caption-loose"]/@href').getall()
		for cat in categories:
			yield response.follow(cat, self.parse_category)


	def parse_category(self, response):
		category_name = response.xpath('//h1/text()').get()
		links = response.xpath('//div[@class="jsx-3498974827 content"]//a[@class="jsx-1191953325 jsx-4098142206 font-caption-loose"]/@href').getall()
		for link in links:
			yield response.follow(link, self.parse_post, cb_kwargs=dict(category_name=category_name))

		next_page = response.xpath('//a[@class="jsx-3498974827 "]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse_category)


	def parse_post(self, response, category_name):
		title = response.xpath('//h1/span/text()').get()
		content = response.xpath('//div[@class="jsx-3211220463 contentWrapper"]//text()[not (ancestor::style)]').getall()
		content = re.sub(pattern, "",' '.join(content))
		content = w3lib.html.remove_tags(content)
		emoji_pattern = re.compile("["
								   u"\U0001F600-\U0001F64F"  # emoticons
								   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
								   u"\U0001F680-\U0001F6FF"  # transport & map symbols
								   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
								   "]+", flags=re.UNICODE)
		content = emoji_pattern.sub(r'', content)

		date = response.xpath('//p[@class="jsx-3211220463 meta"]//text()').getall()[0]

		item = ItemLoader(item=Bank99Item(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('category', category_name)
		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
