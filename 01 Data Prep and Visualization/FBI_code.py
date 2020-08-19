# Crawl data from Chicago Police Department Clear Map Crime Summary

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

# This restores the same behavior as before.
context = ssl._create_unverified_context()

def get_FBI_code():
    '''
    Get a list of information from crawl data from Chicago Police Department
    Clear Map Crime Summary

    Inputs:

    Returns: dictionary
    '''
    # return soup with class = "def"
    page = get_page("http://gis.chicagopolice.org/clearmap_crime_sums/crime_types.html#N14")
    soup = BeautifulSoup(page, "html.parser")
    crimes_type = get_body(soup, "td", "def")

    # return list of body information
    information = []
    for item in crimes_type:
        info = get_info(item)
        information.append(info)

    # decide whether to include the information
    useful_information = []
    for item in information:
        if '(Crime Against Property)' in item:
            useful_information.append(item)
        elif '(Crime Against Society)' in item:
            useful_information.append(item)
        elif '(Crimes Against Persons and Society)' in item:
            useful_information.append(item)
        elif '(Crimes Against Persons)' in item:
            useful_information.append(item)
        elif '(Crimes Against Property)' in item:
            useful_information.append(item)
        elif '(Crimes Against Society)' in item:
            useful_information.append(item)

    # format, clean the information and convert to dict
    FBI_code_list = []
    for item in useful_information:
        item = item.replace("(Index)", "")
        item = item.replace("Crimes", "Crime")
        item = re.findall('\((.*?)\)', item)
        FBI_code_list.append(item)
        FBI_code_dict = {d[0]: d[1] for d in FBI_code_list}

    return FBI_code_dict


def get_page(url):
    '''
    Check the page ready for crawl

    Inputs:
        url: web page url

    Returns: string (check if page can crawl)
    '''
    fd = urlopen(url, context=context)
    content = fd.read()
    fd.close()
    return content.decode('utf8')


def get_body(soup, name, class_type):
    '''
    Get the body

    Inputs:
        soup: a crawled page
        name: tag
        class_type: class type

    Returns: soup
    '''
    return soup.find_all(name, {'class' : class_type})


def get_info(soup):
    '''
    Get the body inside tag

    Inputs:
        soup: a crawled page

    Returns: list of string text
    '''
    return soup.text


if __name__ == "__main__":
    get_FBI_code()
