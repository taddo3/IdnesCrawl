from requests import get
from re import search, sub
from json import dumps


def get_title(text):
    result = search('(?<=<title>)[^<]+', text)
    if result:
        result = result.group()
        return result
    else:
        return ''


def get_datetime(text):
    result = search('article: *published_time" +content *= *"[^"]+', text)
    if result:
        result = result.group()
        result = sub('article: *published_time" +content *= *"', '', result)
        return result
    else:
        return ''


def get_category(text):
    result = search('<li +class *= *"act" +id *= *"[^"]+', text)
    if result:
        result = result.group()
        result = sub('<li +class *= *"act" +id *= *"', '', result)
        return result
    else:
        return ''


def get_authors(text):
    result = search('"authors" *: *\[[^\]]+\]', text)
    if result:
        result = result.group()
        result = sub('("authors" *: *\[)|\]', '', result)
        authors = result.split(',')
        for i in range(len(authors)):
            authors[i] = sub('"', '', authors[i])
        return authors
    else:
        return []


def get_content(text):
    result = search('<!--Modify:artPart0--> *(<[a-z0-9]+>)* *[^<]+', text)
    if result:
        result = result.group()
        result = sub('<!--Modify:artPart0--> *(<[a-z0-9]+>)* *', '', result)
        return result
    else:
        return ''


def get_subcategory(text):
    result = search('<li *class *= *"act" *> *<[^>]+>[^<]+', text)
    if result:
        result = result.group()
        result = sub('<li *class *= *"act" *> *<[^>]+>', '', result)
        return result
    else:
        return ''


def get_headline(text):
    result = search('<div *class *= *"opener" *>[^<]+', text)
    if result:
        result = result.group()
        result = sub('(<div *class *= *"opener" *>\r\n *)|( *\r\n *)', '', result)
    return result


def get_data(article_url):
    data = dict()
    article_response = get(article_url)
    if article_response.status_code == 200:
        data['title'] = get_title(article_response.text)
        data['datetime'] = get_datetime(article_response.text)
        data['category'] = get_category(article_response.text)
        data['authors'] = get_authors(article_response.text)
        data['content'] = get_content(article_response.text)
        data['subcategory'] = get_subcategory(article_response.text)
        data['headline'] = get_headline(article_response.text)
    return data


class ArticleScraper:

    def __init__(self, file_name):
        self.file_name = file_name

    def scrap_article(self, article_url):
        data = get_data(article_url)
        if data:
            with open(self.file_name, 'a+', encoding='utf-8') as f:
                f.write(dumps(data, indent=4, sort_keys=True))

