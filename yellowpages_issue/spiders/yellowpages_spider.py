"""
Spider to scrap review from `yellowpages.com`.
"""
# pylint: disable=

# import json
# from w3lib.url import url_query_cleaner
import scrapy

# from ..utils import (create_search_query, extract_text, nowts, parse_date_ts,
#                      select_result, url_params)
# from .base import BaseReviewsSpider


class YellowpagesSpider(scrapy.Spider):
    """ Web Spider class for Yellow Pages """

    name = 'yellowpages-spider'
    allowed_domains = ['yellowpages.com','dexknows.com',"superpages.com"]

    search_results_found = 0
    reached_business_page = False
    # def search_requests(self):


    fh = open('SP1905_D.txt','r')
    data = fh.read()
    start_urls = data.split(',')

    def parse(self,response):
        # scrapy.shell.inspect_response(response,self)
        
        yield {
            'request_url':response.request.meta['redirect_urls'][0] if response.request.meta.get('redirect_urls') else response.request.url,
            'response_url':response.url,
            'address_found':"yes" if response.css('.address') else "no",
        }



    # def parse_search_results(self, response):  #needsChange
    #     """ This method will parrse search result """

    #     def get_address(result):
    #         """ This method will get address """
    #         address_parts = result.xpath('.//div[@class="adr"]//text()').extract()
    #         if address_parts:
    #             address = filter(None, [
    #                 e.strip().strip(', ')
    #                 for e in
    #                 address_parts
    #             ])
    #         else:
    #             address = []
    #             street_address = result.xpath(
    #                 './/div[@class="street-address"]//text()').extract_first()
    #             locality = result.xpath('.//div[@class="locality"]//text()').extract_first()
    #             if street_address:
    #                 address.append(street_address)
    #             if locality:
    #                 address.append(locality)
    #         return u', '.join(address)

    #     results = response.css('.search-results.organic .info, .category-expansion .info')
    #     self.search_results_found = len(results)
    #     compare_targets = [dict(
    #         name=extract_text(r.css('h2 a')),
    #         text=get_address(r)) for r in results if r.css('div.adr').extract_first()]

    #     try:
    #         if compare_targets[0]['text'] == [] or compare_targets[0]['text'] == '':
    #             self.logger.warning('Not getting addresses of businesses to compare with inputed '
    #                                 'business from search page.')
    #     except (TypeError, IndexError):
    #         self.logger.warning('Not getting names and addresses of businesses to compare with '
    #                             'inputed business from search page.')

    #     result_index = select_result(self.place, compare_targets)
    #     if result_index is not None:
    #         result = results[result_index]
    #         link = result.css('h2 a::attr(href)').extract_first()
    #         if link:
    #             url = url_query_cleaner(response.urljoin(link))
    #             self.profile_key = url
    #             self.logger.info('Found profile URL: %s' % url)
    #             yield scrapy.Request(url, self.parse_business_page)

    # def parse_business_page(self, response):  #needsChange
    #     """ This method will parse business page """
    #     self.reached_business_page = True
    #     if self.histogram is None:
    #         self.get_review_histogram(response)

    #     reviews_list = response.xpath(
    #         '//article[.//*[@itemprop="itemReviewed"]]')
    #     reviews_list_two = response.xpath(
    #         '//div[@id="reviews-container"]//article[@id]')
    #     self.logger.info('Reviews list two length: %s' % len(reviews_list_two))
    #     if reviews_list != []:
    #         self.minimal_review_count = len(reviews_list)
    #         for review in reviews_list:
    #             source_date = extract_text(
    #                 review.xpath('.//*[@itemprop="dateCreated"]'))
    #             rating = review.xpath(
    #                 './/*[@itemprop="ratingValue"]/@content').extract_first()
    #             yield {
    #                 'author_name': extract_text(review.xpath('.//*[@itemprop="author"]')),
    #                 'text': extract_text(review.xpath('.//*[@itemprop="reviewBody"]')),
    #                 'source_date': source_date,
    #                 'rating': float(rating) if rating is not None else None,
    #                 'posted_at': parse_date_ts(source_date),
    #                 'scraped_at': nowts(),
    #             }

    #         pages = response.css('.pagination a::text').extract()
    #         total_pages = max(int(x)
    #                           for x in pages if x.isdigit()) if pages else 1
    #         cur_page = response.css(
    #             '.pagination a.current::text').extract_first()
    #         cur_page = int(cur_page) if cur_page else 0
    #         if cur_page and cur_page <= total_pages:
    #             self.logger.info(
    #                 'Pagination: currently on page %s of %s' %
    #                 (cur_page, total_pages))
    #             url = url_params(response.url, page=str(cur_page + 1))
    #             yield scrapy.Request(url, self.parse_business_page)

    #     elif reviews_list_two != []:
    #         self.minimal_review_count = len(reviews_list_two)
    #         for review in reviews_list_two:
    #             review_id = review.css('article::attr(id)').extract_first()
    #             source_date = extract_text(review.css('p.date-posted > span'))
    #             if not source_date:
    #                 date = review.css(
    #                     'span.date-posted').re(r'\d{1,2}\/\d{1,2}\/\d{4}')
    #                 if date:
    #                     source_date = date[0]
    #             rating_string = review.css(
    #                 '.rating-indicator::attr(class)').re_first(r'rating-indicator (\w+) ')
    #             data_map = {
    #                 'one': 1,
    #                 'two': 2,
    #                 'three': 3,
    #                 'four': 4,
    #                 'five': 5
    #             }
    #             rating = None
    #             if rating_string is not None and data_map[rating_string] is not None:
    #                 rating = data_map[rating_string]

    #             fetched_review = {
    #                 'review_id': review_id,
    #                 'url': u'{}?review={}#reviews'.format(
    #                     self.profile_key,
    #                     review_id),
    #                 'author_name': extract_text(
    #                     review.css('.author')),
    #                 'text': extract_text(
    #                     review.css('div.review-response')),
    #                 'source_date': source_date,
    #                 'rating': float(rating) if rating is not None else None,
    #                 'posted_at': parse_date_ts(source_date),
    #                 'scraped_at': nowts(),
    #             }

    #             if review.css('.author::attr(href)'):
    #                 author_id = review.css(
    #                     '.author::attr(href)').extract_first()
    #                 if '/reviews' in author_id:
    #                     author_id = author_id.replace('/reviews', '')
    #                 fetched_review['author_id'] = author_id

    #             yield fetched_review
    #         pages = response.css('.pagination a::text').extract()
    #         total_pages = max(int(x)
    #                           for x in pages if x.isdigit()) if pages else 1
    #         cur_page = response.css(
    #             '.pagination a.current::text').extract_first()
    #         cur_page = int(cur_page) if cur_page else 0
    #         self.logger.info(
    #             'Pagination: scraped page %s of %s' %
    #             (cur_page, total_pages))
    #         if cur_page and cur_page < total_pages and not self.first_page_only:
    #             url = url_params(response.url, page=str(cur_page + 1))
    #             yield scrapy.Request(url, self.parse_business_page)

    # # def get_review_histogram(self, response):
if __name__ == "__main__":
    fh = open('SP1905_S.txt','r')
    data = fh.read()
    print(data.split(','))
