import requests
import re
from lxml import html
from multiprocessing import Pool
from lxml import etree
import json
from swissjur.source import TF_CONF

ATF_INDEX_URL="https://www.bger.ch/ext/eurospider/live/fr/php/clir/http/index_atf.php"
CREDH_LIST_URL="https://www.bger.ch/ext/eurospider/live/fr/php/clir/http/index_cedh.php?lang=fr"

ATF_DOC_URL="https://www.bger.ch/ext/eurospider/live/fr/php/clir/http/index.php?lang=fr&type=show_document&highlight_docid=atf://{docid}:{lang}&print=yes"

TABLE_HREF_XPATH='//table/tr/td/a/@href'
ORDERED_LIST_HREF_XPATH='//div/ol/li/a/@href'
DOC_XPATH="//div[@id='highlight_content']"

def get_year_pages_on_list_of_atf_page():
    return filter(
        lambda x: x.startswith(ATF_INDEX_URL), # remove non ATF pages
        query_and_xpath(
            ATF_INDEX_URL,
            TABLE_HREF_XPATH,
        )
    )

def get_atf_link_from_year_page(year_page):
    return query_and_xpath(
        year_page,
        ORDERED_LIST_HREF_XPATH,
    )

def get_credh_links():
    return query_and_xpath(
        CREDH_LIST_URL,
        TABLE_HREF_XPATH,
    )[::2] # each link appears twice on the same row

def get_atf_document_content(atf_id, lang='fr'):
    atf_link = ATF_DOC_URL.format(
        docid=atf_id,
        lang='fr'
    )
    node = query_and_xpath(
        atf_link,
        DOC_XPATH,
    )
    assert len(node) == 1
    return etree.tostring(node[0])

def get_all_atf_links(n_threads=4):
    if n_threads < 1:
        raise ValueError(
            "Invalid input : n_threads should be > 1, got " + str(n_threads))
    year_pages = get_year_pages_on_list_of_atf_page()
    
    links = None
    if n_threads > 1:
        p = Pool(n_threads)
        links = p.map(get_atf_link_from_year_page, year_pages)
    else:
        links = map(get_atf_link_from_year_page, year_pages)

    return reduce(list.__add__, links)

def extract_atf_id(link):
    return re.search('highlight_docid=atf%3A%2F%2F(.*)%3A&', link).group(1)

def get_all_atf_ids():
    links = get_all_atf_links(n_threads=4)
    return map(extract_atf_id, links)

def query_and_xpath(url, xpath):
    page = requests.get(url)
    return html.fromstring(
        page.content
    ).xpath(
        xpath
    )

if __name__ == "__main__":
    print(get_all_atf_ids())
