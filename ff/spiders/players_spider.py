import scrapy

class PlayersSpider(scrapy.Spider):
	name = 'players'

	start_urls = ['https://www.pro-football-reference.com/players/']

	def parse(self, response):
		for letter_href in response.css('ul.page_index li > a::attr(href)').extract():
			yield response.follow(letter_href, self.parse_position)

	def parse_position(self, response):
		for player in response.css('div.section_content p b'):
			player_name = player.css('a::text').extract_first()
			position = player.css('::text').re(r'\(([^)]+)\)')[0]
			href = player.css('a::attr(href)').extract_first()
			yield response.follow(href, self.parse_player, meta={'position' : position, 'player_name' : player_name})

	def parse_player(self, response):
		position = response.meta['position']
		player_name = response.meta['player_name']
		for game in response.xpath('//table[@id="stats"]/tbody/tr[contains(@id, "stats")]'):
			if position == "WR":
				yield{

				#WHAT ABOUT PUNT / KICKOFF RETURNS?

					'player_name' : player_name,
					#'game_date' : game.xpath('td[contains(@data-stat, "game_date")]/a/text()').extract_first(),
					'week_num' : game.xpath('td[contains(@data-stat, "week_num")]/text()').extract_first(),
					'team' : game.xpath('td[contains(@data-stat, "team")]/a/text()').extract_first(),
					'targets' : game.xpath('td[contains(@data-stat, "targets")]/text()').extract_first(),
					'rec' : game.xpath('td[contains(@data-stat, "rec")]/text()').extract_first(),
					'rec_yds' : game.xpath('td[contains(@data-stat, "rec_yds")]/text()').extract_first(),
					'rec_tds' : game.xpath('td[contains(@data-stat, "rec_td")]/text()').extract_first(),
					'rush_att' : game.xpath('td[contains(@data-stat, "rush_att")]/text()').extract_first(),
					'rush_yds' : game.xpath('td[contains(@data-stat, "rush_yds")]/text()').extract_first(),
					'rush_td' : game.xpath('td[contains(@data-stat, "rush_td")]/text()').extract_first()
				}
