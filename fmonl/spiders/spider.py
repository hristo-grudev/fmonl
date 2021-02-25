import scrapy

from scrapy.loader import ItemLoader
from ..items import FmonlItem
from itemloaders.processors import TakeFirst


class FmonlSpider(scrapy.Spider):
	name = 'fmonl'
	start_urls = ['https://www.fmo.nl/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="u-NewsItemGridView__table TitleBlock__container"]')
		for post in post_links:
			link = post.xpath('./a/@href').get()
			date = post.xpath('.//span[@class="TitleBlock__date"]/text()').get()
			yield response.follow(link, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h2[@class="at-header__mainTitle"]/text()').get()
		description = response.xpath('//div[@class="NewsItemDetailView__content"]//text()[normalize-space()]|//div[@class="at-asideArticle__content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=FmonlItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
