import scrapy


class ThreadsSpider(scrapy.Spider):
    name = "threads"
    # scrape Bitcoin, Ethereum, and Ethereum Classic top posts of all time
    start_urls = [
        'https://www.reddit.com/r/ethereum/top/?sort=top&t=all'
        # 'https://www.reddit.com/r/Bitcoin/top/?sort=top&t=all'
        # 'https://www.reddit.com/r/EthereumClassic/top/?sort=top&t=all'
    ]

    # For each entry on a public-facing subreddit page, pull title, author, relative time, entire time group, tagline, and comments
    def parse(self, response):
        for thread in response.css('div.entry.unvoted'):
            yield {
                'title': thread.css('a.title.may-blank::text').extract_first(),
                'author': thread.css('a.author.may-blank::text').extract_first(),
                'time_rel': thread.css('time::text').extract_first(),
                'time_all': thread.css('time').extract_first(),
                'tagline': thread.css('p.tagline::text').extract_first(),
                'comments': thread.css('a.bylink.comments.may-blank::text').extract_first(),
            }

        # Go to next page if their is a 'next-button' on current page
        next_page = response.css('span.next-button a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
