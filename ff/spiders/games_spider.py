import scrapy

class gamesSpider(scrapy.Spider):
	name = "games"
	start_urls = ['https://www.pro-football-reference.com/years/']
	def parse(self, response):
		#years_array = ['2018','2017','2016','2015','2014','2013','2012']
		years_array = ['2018','2017']
		weeks_array = ['week_1','week_2','week_3']
		for year in years_array:
			for week in weeks_array:
				href = year + '/' + week + '.htm'
				yield response.follow(href, self.parse_week, meta={'year':year, 'week':week})


	def parse_week(self, response):
		year = response.meta['year']
		week = response.meta['week']

		for game in response.xpath('//div[@class="game_summaries"]/div[@class="game_summary expanded nohover"]/table[@class="teams"]//tr[2]'):
			href = game.xpath('td[@class="right gamelink"]/a/@href').extract_first()
			yield response.follow(href, self.parse_game, meta={'year':year, 'week':week})

	def parse_game(self, response):
		year = response.meta['year']
		week = response.meta['week']

		yield {
			'test' : response.url
		}
