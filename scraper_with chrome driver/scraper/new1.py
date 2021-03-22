from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as soup
import requests
import json
import csv
from csv import writer
import re
import socket
from socket import timeout
import socket
import errno
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import ssl
from urllib.parse import urlparse
from selenium import webdriver
import tldextract

cate = ['contact', 'about']
emailD = []
product_links = []
competitors = ['patientfusion.csv']


def check_duplicate_product(origin, product):
    info_origin = tldextract.extract(origin)
    info_product = tldextract.extract(product)
    return info_origin.domain != info_product.domain or info_origin.suffix != info_product.suffix


def check_dup(liste, e):
    val = True
    for elliment in liste:
        if e == elliment:
            val = False
            return val
    return val


def get_email(url):

    if not url.endswith('/'):
        url = url+'/'
    browser = webdriver.Chrome()
    try:
        print(url)
        emailD.append(url)
        browser.get(url)
        source = browser.page_source
        content = BeautifulSoup(source, "html.parser", from_encoding="utf-8", exclude_encodings=["latin-1", "ISO-8859-7"])
        # book_links = content.select('a[href^=http]')
        # product_link = []
        # for book_link in book_links:
        #     temp = book_link(text=True)
        #     if len(temp) > 0:
        #         temp = temp[0]
        #         if (
        #                 'book' in temp.lower() or 'schedule' in temp.lower() or 'appointment' in temp.lower()) and check_duplicate_product(
        #                 url, book_link['href']) and 'facebook' not in book_link['href'].lower():
        #             product_link = book_link['href']
        #             break
        # if len(product_link) > 0:
        #     product_links.append(product_link)

        mailtos = content.select('a[href^=mailto]')
        for i in mailtos:
            href = i['href']
            try:
                str1, str2 = href.split(':')
                if str2.find('?') != -1:
                    str3, str4 = str2.split('?')
                    str2 = str3
            except ValueError:
                break
            if check_dup(emailD, str2) == True:
                emailD.append(str2)
                print(str2)
        html_text = str(content)
        mail_list = re.findall('\w+@\w+\.com', html_text)
        for mail in mail_list:
            if check_dup(emailD, mail) == True:
                emailD.append(mail)
                print(mail)

        for i in range(2):
            new_url = ''
            links = content.findAll('a', href=re.compile(cate[i]))
            for link in links:
                if link.get('href').startswith('mailto'):
                    break
                if link.get('href').startswith('http'):
                    if link.get('href').endswith('/'):
                        new_url = link.get('href')
                    else:
                        new_url = link.get('href') + '/'
                else:
                    if link.get('href').startswith('/'):
                        if link.get('href').endswith('/'):
                            new_url = url[:-1] + link.get('href')
                        else:
                            new_url = url[:-1] + link.get('href') + '/'
                    else:
                        if link.get('href').endswith('/'):
                            new_url = url + link.get('href')
                        else:
                            new_url = url + link.get('href') + '/'
                sub_search(new_url)
                break
    except:
        print("error")
    browser.close()


class MyException(Exception):
    pass


def sub_search(url):
    browser = webdriver.Chrome()
    try:
        print(url)
        browser.get(url)
        source = browser.page_source
        content = BeautifulSoup(source, "html.parser", exclude_encodings=["latin-1"])
        # book_links = content.select('a[href^=http]')
        # product_link = ''
        # for book_link in book_links:
        #     temp = book_link(text=True)
        #     if len(temp) > 0:
        #         temp = temp[0]
        #         if ('book' in temp.lower() or 'schedule' in temp.lower() or 'appointment' in temp.lower()) and check_duplicate_product(url, book_link['href']) and 'facebook' not in book_link['href'].lower():
        #             product_link = book_link['href']
        #             break
        # if len(product_link) > 0:
        #     product_links.append(product_link)

        mailtos = content.select('a[href^=mailto]')
        for i in mailtos:
            href = i['href']
            try:
                str1, str2 = href.split(':')
                if str2.find('?') != -1:
                    str3, str4 = str2.split('?')
                    str2 = str3
            except ValueError:
                break
            if check_dup(emailD, str2) == True:
                emailD.append(str2)
                print(str2)
        html_text = str(content)
        mail_list = re.findall('\w+@\w+\.com', html_text)
        for mail in mail_list:
            if check_dup(emailD, mail) == True:
                emailD.append(mail)
                print(mail)
    except:
        print("error")
    browser.close()


def add_email(filename, list_email):
    with open(filename, 'a+', newline='', encoding='utf-8') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_email)

def process(target, competitor):
    get_email(target)
    # for index in range(len(product_links)):
    #     emailD.append(product_links[index])
    add_email(competitor, emailD)


for competitor in competitors:
    with open("./backlists/" + competitor, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            emailD = []
            product_links = []
            url = row[0]
            process(url, competitor)
