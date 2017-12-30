import requests
import re
from lxml import html
from multiprocessing import Pool
from lxml import etree
import json
from swissjur.source import TF_CONF

def get_year_pages_on_list_of_atf_page():
    return filter(
        lambda x: x.startswith(TF_CONF['ATF_INDEX']['url']), # remove non ATF pages
        query_and_xpath(
            TF_CONF['ATF_INDEX']['url'],
            TF_CONF['ATF_INDEX']['XPATH'],
        )
    )

def get_atf_link_from_year_page(year_page):
    return query_and_xpath(
        year_page,
        TF_CONF['ATF_YEAR_PAGE']['XPATH'],
    )

def get_credh_links():
    return query_and_xpath(
        TF_CONF['CREDH_INDEX']['url'],
        TF_CONF['CREDH_INDEX']['XPATH'],
    )[::2] # each link appears twice on the same row

def get_atf_document_content(atf_id, lang='fr'):
    node = query_and_xpath(
        TF_CONF['ATF_DOC']['url'].format(
            docid=atf_id,
            lang=lang,
        ),
        TF_CONF['ATF_DOC']['XPATH'],
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

