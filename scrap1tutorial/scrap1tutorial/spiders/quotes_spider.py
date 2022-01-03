import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        # for url in urls:
        #     yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
        for quote in response.css('.quote'):
            yield {
                # 'text': quote.css('span.text::text').get(),
                # 'author': quote.css('small.author::text').get(),
                # 'tags': quote.css('div.tags a.tag::text').getall(), #from website
                'text':quote.css('.text::text').get(),
                'author':quote.css('.author::text').get(),
                'tags':quote.css('.tags .tag::text').getall(),
            }

        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,self.parse)