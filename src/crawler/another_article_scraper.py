from requests import get
from re import search, sub
from json import dumps
from os import path


# Function bellow extract the specific parts from an article html response.
def get_title(text):
    result = search('(?<=<title>)[^<]{10,}', text)
    if result:
        result = result.group()
        return result
    else:
        return ''


def get_datetime(text):
    result = search('"dateOfPublication":"[^"]+', text)
    if result:
        result = result.group()
        result = sub('"dateOfPublication":"', '', result)
        return result
    else:
        return ''


def get_category(text):
    result = search('\.cz\/[^\/]+', text)
    if result:
        result = result.group()
        result = sub('\.cz\/', '', result)
        return result
    else:
        return ''


def get_authors(text):
    result = search('"Person","name":"[^"]+', text)
    if result:
        result = result.group()
        result = sub('"Person","name":"', '', result)
        return [result]
    else:
        return []


def get_content(text):
    result = search('"properties":\{"texts":\["[^"]+', text)
    if result:
        result = result.group()
        result = sub('"properties":\{"texts":\["', '', result)
        return result
    else:
        return ''


def get_headline(text):
    result = search('name="description" content="[^"]+', text)
    if result:
        result = result.group()
        result = sub('name="description" content="', '', result)
    return result


def get_data(article_url):
    """
    This is function for calling other functions to extract specific parts of an article html response.
    Return a dictionary with extracted data.
    """
    try:
        article_response = get(article_url)
    except Exception as ex:
        print('Error: ' + str(ex))
        return None

    if article_response.status_code == 200:
        data = dict()
        data['title'] = get_title(article_response.text)
        data['datetime'] = get_datetime(article_response.text)
        data['category'] = get_category(article_url)
        data['authors'] = get_authors(article_response.text)
        data['headline'] = get_headline(article_response.text)
        data['content'] = get_content(article_response.text)
        return data


class AnotherScraper:

    def __init__(self, file_name, max_file_size):
        self.file_name = file_name
        self.max_file_size = max_file_size
        if not path.exists(self.file_name):
            with open(self.file_name, 'w', encoding='utf-8') as f:
                f.close()

    def scrap_article(self, article_url):
        """
        This method retrieve data from article url and store this data as json in specific file.
        """
        data = get_data(article_url)
        if data:
            json = dumps(data, indent=4, sort_keys=True)
            if path.getsize(self.file_name) + len(json) > self.max_file_size:
                next_file_number = int(sub('[^0-9]', '', self.file_name)) + 1
                self.file_name = sub('[0-9]+', str(next_file_number), self.file_name)
            with open(self.file_name, 'a+', encoding='utf-8') as f:
                f.write(json + '\n')
            print('Scraped: ' + article_url)

