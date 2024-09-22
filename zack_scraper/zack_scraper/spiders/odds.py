import scrapy

class OddsSpider(scrapy.Spider):
    name = "leagues_odds"
    countries = ["germany", "england", "france"]
    start_urls = [f"https://www.oddsportal.com/football{country}" for country in countries]

    def parse(self, response, countries):
        urls_to_scrape = self.makeLeagueUrls(response=response.url)

        yield urls_to_scrape

    def makeLeagueUrls(self, response):
        leagues_url_paths = response.xpath('//a[@class="font-main font-normal text-xs text-black-main underline"]/@href').getall()

        leagues_urls = [f"{response.url}{league.split('/')[3]}/results/" for league in leagues_url_paths]

        return leagues_urls[0:5]






