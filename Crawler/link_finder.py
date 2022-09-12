import urllib
import tldextract
from html.parser import HTMLParser
from urllib.parse import urljoin

class link_crawler(HTMLParser):

    def __init__(self, start_link, web_url):
        super().__init__()
        self.start_link = start_link
        self.web_url = web_url
        self.urls = set()

    def handle_starttag(self, tag, found_attributes):     # The main logic for crawler
        if tag == 'a':
            for (attr, value) in found_attributes:
                if attr == 'href':
                    url = urllib.parse.urljoin(self.start_link, value)
                    url_extract = tldextract.extract(url)
                    site_suff = '.' + url_extract.suffix
                    if site_suff=='.onion':
                        self.urls.add(url)

    def page_urls(self):
        return self.urls

    def error(self, message):
        pass