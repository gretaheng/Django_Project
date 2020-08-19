# Crawl data from University of Chicago security alerts archive

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl
import csv


# This restores the same behavior as before.
context = ssl._create_unverified_context()

# regular expression
reg = re.compile('\S{4,}')
time = '([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'
pm_am = '(p\.m\.)|(a\.m\.)'
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_re = '|'.join(days)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']
months_re = '|'.join(months)
time_re = '(%s) (%s),? (%s), (%s) [0-9]*' % (time, pm_am, days_re, months_re)
title_time_re = '(%s), (%s) [0-9]*, [0-9]*' % (days_re, months_re)
capitalized_word_re = ' [A-Z][a-zA-Z.]*'
numbered_street = ' [0-9]+[a-z]*'
address_re = '\d{1,4}((%s)|(%s))+ (Avenue|Street|Place)' % (capitalized_word_re,
                                                            numbered_street)
address_re_2 = '((%s)|(%s))+ between \w+ (Avenue|Street|Place) and \w+ (Avenue|' \
               'Street|Place)' % (capitalized_word_re, numbered_street)
address_re_3 = '\d+\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))'
address_re_4 = '\d+\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))\s(near)' \
               '\s\d+\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))'
address_re_5 = '\d+|\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))\s(and)' \
               '(\s\d+|)\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))'
address_re_6 = '\d+|\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))'
address_re_7 = '\d+|\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))\s(near)' \
               '(\s\d+|)\s(((\d|)+(st|nd|rd|th))|[A-z])+\s((Street|Avenue|Place))'
address_re_8 = '\d+|\s(East|West|North|South)\s(((\d|)+(st|nd|rd|th))|[A-z])' \
               '+\s((Street|Avenue|Place))'


def get_security_alert():
    '''
    Get information form the website

    Inputs:

    Returns: list
    '''
    page = get_page("https://safety-security.uchicago.edu/services/security_alerts/")
    soup = BeautifulSoup(page, "html.parser")
    links = get_links(soup)

    title_info = []
    useful_body_info = []

    for link in links:
        link = BeautifulSoup(link, "html.parser")

        body = get_body(link)
        for single_body in body:
            title = get_title(single_body)
            useful_body = get_useful_body(single_body)

        title_info.append(title)
        useful_body_info.append(useful_body)

    return title_info, useful_body_info


def edit_security_alert():
    '''
    Edit soup body

    Inputs:

    Returns: list
    '''
    title_info, useful_body_info = get_security_alert()
    merged_list = to_string(title_info, useful_body_info)
    return merged_list


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


def get_links(soup):
    '''
    Get the sub links and crawl the sub links

    Inputs:
        soup: a crawled page

    Returns: soup
    '''
    article = soup.find_all('article', class_="span9 main")[0]
    links = []
    for link in article.find_all('a'):
        sub_link = link.get('href')
        if 'update' not in sub_link:
            sub_page = get_page("https://safety-security.uchicago.edu/services/security_alerts/" + sub_link)
            links.append(sub_page)
    return links


def get_body(soup):
    '''
    Get the body

    Inputs:
        soup: a crawled page

    Returns: soup
    '''
    return soup.find_all('article', class_="span6 main")


def get_title(soup):
    '''
    Get the title

    Inputs:
        soup: a crawled page

    Returns: soup
    '''
    temp = soup.find_all('h2')
    return temp


def get_useful_body(soup):
    '''
    Get the body

    Inputs:
        soup: a crawled page

    Returns: soup
    '''
    children = []
    temp = soup.find_all('p')
    for child in temp:
        sub_title = child.find_all('strong')
        if len(sub_title) > 0:
            children.append(child)
    return children


def to_string(list1, list2):
    '''
    Merge and convert to string

    Inputs:
        list1: list
        list2: list

    Returns: nre_list
    '''
    new_list = []
    for i in range(len(list1)):
        list1[i] = str(list1[i])
        list2[i] = str(list2[i])
        if "Update" not in list1[i]:
            merged = (list1[i], list2[i])
            new_list.append(merged)
    return new_list


def toTwo(num):
    '''
    Check the num

    Inputs:
        num: int

    Returns: string
    '''
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)


def extract():
    '''
    Export CSV file, take out time, date, and address

    Inputs:

    Returns: csv
    '''
    to_extract = edit_security_alert()
    result = []
    for text in to_extract:

        # extract time
        year = re.search(title_time_re, text[0]).group(0).split(' ')[-1]
        search_result = re.search(time_re, text[1])
        if search_result == None:
            search_result = re.search(time_re, text[0])
        if search_result != None:
            raw_time = search_result.group(0)

            # extract date
            date = raw_time.split(',')[-1][1:]
            month = date.split(' ')[0]
            day = date.split(' ')[1]
            for i in range(12):
                if month == months[i]:
                    month = i + 1
                    break

            # extract time
            splitted = raw_time.split(' ')
            hour = int(splitted[0].split(':')[0])
            minute = int(splitted[0].split(':')[1])
            if splitted[1].split(',')[0] == 'p.m.':
                hour += 12

            line = [raw_time + ', ' + year, year + toTwo(month) + toTwo(int(day)),
                    toTwo(hour) + toTwo(minute)]
        else:
            line = ['', '', '']

        search_result = re.search(address_re, text[1])
        search_2 = re.search(address_re_2, text[1])
        search_3 = re.search(address_re_3, text[1])
        search_4 = re.search(address_re_4, text[1])
        search_5 = re.search(address_re_5, text[1])
        search_6 = re.search(address_re_6, text[1])
        search_7 = re.search(address_re_7, text[1])
        search_8 = re.search(address_re_8, text[1])
        if search_result != None:
            line.append(search_result.group(0))
        elif search_2 != None:
            line.append(search_2.group(0))
        elif search_3 != None:
            line.append(search_3.group(0))
        elif search_4 != None:
            line.append(search_4.group(0))
        elif search_5 != None:
            line.append(search_5.group(0))
        elif search_6 != None:
            line.append(search_6.group(0))
        elif search_7 != None:
            line.append(search_7.group(0))
        elif search_8 != None:
            line.append(search_8.group(0))
        else:
            line.append('')

        result.append(line)

    with open('security.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Raw_Time', 'Date', 'Time', 'Address'])
        writer.writerows(result)


if __name__ == "__main__":
    extract()




