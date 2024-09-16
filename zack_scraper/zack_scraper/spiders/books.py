class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://books.toscrape.com/',
    ]

    def parse(self, response):
        total_pages = int(current.split("\n")[2].lstrip().split(' ')[-1])
        page_urls = [f"https://books.toscrape.com/catalogue/page-{i}.html" for i in range(1, pages + 1)]

        for page in range(1, total_pages + 1):
            next_page_url = f"http://books.toscrape.com/catalogue/page-{page}.html"
            yield scrapy.Request(url=next_page_url, callback=self.parse_books)

    def parse_books(self, response):
        # Extract book data from each page
        books = response.xpath('//article[@class="product_pod"]')

        for book in books:
            yield {
                'title': book.xpath('.//h3/a/@title').get(),
                'price': book.xpath('.//div[@class="product_price"]/p[@class="price_color"]/text()').get(),
                'availability': book.xpath('.//p[contains(@class, "instock")]/text()').re_first('\S+'),
            }
