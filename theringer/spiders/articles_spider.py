import datetime
import json

import scrapy

from dateutil import relativedelta


class ArticlesSpider(scrapy.Spider):
    name = 'articles'

    def start_requests(self):
        start = datetime.datetime(2015, 11, 30, 23, 59, 59)
        delta = relativedelta.relativedelta(months=1)
        date = datetime.datetime.now() + delta

        while (date := date - delta) > start:
            yield scrapy.Request(
                f'https://www.theringer.com/archives/{date.year}/{date.month}',
                callback=self.parse,
            )

    def parse(self, response):
        for selector in response.css('h2.c-entry-box--compact__title'):
            yield scrapy.Request(
                selector.css('a').attrib['href'],
                callback=self.parse_article,
            )

        if response.css('button.c-archives-load-more__button'):
            site = 'https://www.theringer.com'
            year, month = response.url.split('/')[-2:]
            results = response.css(
                'h1.p-page-title::text'
            ).re_first(r'.*\s\((\d+)\)$')
            pages = 1 + (int(results) - 1) // 30
            for page in range(1, pages):
                yield scrapy.Request(
                    f'{site}/fetch/archives/{year}/{month}/{page + 1}',
                    callback=self.parse_json,
                    headers={'referer': response.url, 'accept': '*/*'},
                )

    def parse_json(self, response):
        response = scrapy.Selector(text=json.loads(response.text)['html'])
        for selector in response.css('h2.c-entry-box--compact__title'):
            yield scrapy.Request(
                selector.css('a').attrib['href'],
                callback=self.parse_article,
            )

    def parse_article(self, response):
        yield {
            'href': response.url,
            'id': self.get_id(response),
            'title': self.get_title(response),
            'description': self.get_description(response),
            'image': self.get_image(response),
            'tags': self.get_tags(response),
            'groups': self.get_groups(response),
            'author': self.get_author(response),
            'date': self.get_date(response),
            'content': self.get_content(response),
        }

    @staticmethod
    def get_id(response):
        link = response.css('span.c-byline__gear').css('a')
        return link.attrib['data-entry-admin'] if link else ''

    @staticmethod
    def get_title(response):
        title = response.css('meta[name="sailthru.title"]')
        return title.attrib['content'] if title else ''

    @staticmethod
    def get_description(response):
        description = response.css('meta[name="sailthru.description"]')
        return description.attrib['content'] if description else ''

    @staticmethod
    def get_image(response):
        image = response.css('meta[name="sailthru.image.full"]')
        return image.attrib['content'] if image else ''

    @staticmethod
    def get_tags(response):
        tags = response.css('meta[name="sailthru.tags"]')
        return tags.attrib['content'] if tags else ''

    @staticmethod
    def get_groups(response):
        return response.css('li.c-entry-group-labels__item').css('a').css(
            'span::text').getall()

    @staticmethod
    def get_author(response):
        return response.css('span.c-byline__author-name::text').get()

    @staticmethod
    def get_date(response):
        date = response.css('meta[name="sailthru.date"]')
        return date.attrib['content'] if date else ''

    @staticmethod
    def get_content(response):
        return '\n\n'.join(
            ''.join(paragraph.css('::text').getall())
            for paragraph in response.css('div.c-entry-content').css('p')
        )
