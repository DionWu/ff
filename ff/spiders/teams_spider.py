import scrapy

class TeamsSpider(scrapy.Spider):
	name = "teams"

	start_urls = ['https://www.pro-football-reference.com/teams/']

	def parse(self, response):
		for team in response.css('div#all_teams_active tbody tr:not([class*="partial_table"])'):
			yield {
				'name' : team.css('th a::text').extract_first(),
				'href' : team.css('th a::attr(href)').extract_first()
			}