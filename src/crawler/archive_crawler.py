from requests import get
from re import findall


class ArchiveCrawler:

    def __init__(self, start_url):
        self.start_url = start_url

    def get_urls(self):
        response = get(self.start_url)

        if response.status_code == 200:
            return findall('[^"]+(?=" +class="art-link">)', response.text)
        else:
            return None
