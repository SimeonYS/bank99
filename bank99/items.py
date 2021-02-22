import scrapy


class Bank99Item(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
