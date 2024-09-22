import scrapy
from scrapy_splash import SplashRequest

class OddsSpider(scrapy.Spider):
    name = "odds"
    start_urls = [f"https://www.oddsportal.com/football/{country}/" for country in ['germany', 'england', 'france']]

    def parse(self, response):
        urls_to_scrape = self.make_league_urls(response=response)

        print(urls_to_scrape)

        for url in urls_to_scrape:
            yield scrapy.Request(url=url, callback=self.parse_leagues)


    def make_league_urls(self, response):
        leagues_url_paths = response.xpath('//a[@class="font-main font-normal text-xs text-black-main underline"]/@href').getall()

        leagues_urls = [f"{response.url}{league.split('/')[3]}-2023-2024/results/#/page/1/" for league in leagues_url_paths]

        pages = response.xpath('//a[@class="pagination-link"]/text()').getall()

        return leagues_urls[0:5]

    def parse_leagues(self, response):
        games = response.xpath('//div[contains(@class, "eventRow")]')

        print(len(games))

        for game in games:
            home_team = game.xpath('.//p[@class="participant-name truncate"]/text()').get()
            away_team = game.xpath('.//p[@class="participant-name truncate"]/text()')[1].get()
            home_score = game.xpath('.//div[@class="min-mt:!flex hidden"]/text()').get()
            away_score = game.xpath('.//div[@class="min-mt:!flex hidden"]/text()')[1].get()

            yield {
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score
            }


