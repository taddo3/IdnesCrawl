from requests import get
from re import findall, sub


class AnotherCrawler:

    start_url = 'https://www.novinky.cz/?timeline-stalose-lastItem=40343844'

    def get_urls(self):
        response = get(self.start_url)

        if response.status_code == 200:
            raw = findall('<a href="[^"0-9]+[0-9]+" class="d_aT', response.text)
            return [sub('" class="d_aT', '', sub('<a href="', '', article)) for article in raw]
        else:
            return None

