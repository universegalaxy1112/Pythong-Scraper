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

cate=['contact','about','visit','Kontakt']

def check_dup(liste,e):
    val=True
    for elliment in liste:
        if e==elliment:
            val=False
            return val
    return val

def get_email(url):
    if url.endswith('/')==False:
        url=url+'/'
    req = Request(url)
    try:
        print(url)
        emailD.append(url)
        context = ssl._create_unverified_context()
        webpage = urlopen(req,timeout=20,context=context).read()

        content = soup(webpage, "html.parser")
        mailtos = content.select('a[href^=mailto]')
        for i in mailtos:
            href=i['href']
            try:
                str1, str2 = href.split(':')
                if str2.find('?') != -1:
                    str3, str4 =  str2.split('?')
                    str2 = str3
            except ValueError:
                break
            if check_dup(emailD,str2)==True:
                emailD.append(str2)
                print(str2)
        html_text = str(content)
        mail_list = re.findall('\w+@\w+\.com', html_text)
        mail=''
        for mail in mail_list:
            if check_dup(emailD,mail)==True:
                emailD.append(mail)
                print(mail)
        
        for i in range(3):
            links=content.findAll('a', href=re.compile(cate[i]))
            new_url=''
            for link in links:
                if link.get('href').startswith('mailto')==True:
                    break
                if link.get('href').startswith('http')==True:
                    if link.get('href').endswith('/')==True:
                        new_url=link.get('href')
                    else:
                        new_url=link.get('href')+'/'
                else:
                    if link.get('href').startswith('/')==True:
                        if link.get('href').endswith('/')==True:
                            new_url=url[:-1]+link.get('href')
                        else:
                            new_url=url[:-1]+link.get('href')+'/'
                    else:
                        if link.get('href').endswith('/')==True:
                            new_url=url+link.get('href')
                        else:
                            new_url=url+link.get('href')+'/'
                print(new_url)
                search(new_url)
                break
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            pass
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            pass
        else:
            print('else')
            pass
    except timeout:
        print('socket timed out - URL %s', url)
        pass
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            get_email(url)
        else:
            raise
    except  http.client.HTTPException as e:
        return("HTTPException")
    except RemoteDisconnected:
        return("RemoteDisconnected")
        pass
class MyException(Exception):
    pass
def search(url):
    req = Request(url)
    try:
        context = ssl._create_unverified_context()
        webpage = urlopen(req,timeout=20,context=context).read()
        content = soup(webpage, "html.parser")
        mailtos = content.select('a[href^=mailto]')
        for i in mailtos:
            href=i['href']
            try:
                str1, str2 = href.split(':')
                if str2.find('?') != -1:
                    str3, str4 =  str2.split('?')
                    str2 = str3
            except ValueError:
                break
            if check_dup(emailD,str2)==True:
                emailD.append(str2)
                print(str2)
        html_text = str(content)
        mail_list = re.findall('\w+@\w+\.com', html_text)
        mail=''
        for mail in mail_list:
            if check_dup(emailD,mail)==True:
                emailD.append(mail)
                print(mail)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            pass
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            pass
        else:
            print('else')
            pass
    except timeout:
        print('socket timed out - URL %s', url)
        pass
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            get_email(url)
        else:
            raise
        pass
    except  http.client.HTTPException as e:
        return("HTTPException")
        pass
    except RemoteDisconnected:
        return("RemoteDisconnected")
        pass
emailD=[]
def add_email(filename,list_email):
    with open(filename, 'a+',newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_email)

def process(url):
    get_email(url)
    if len(emailD)==1:
        add_email('failed_emails.csv',emailD)
    else:
        add_email('emails.csv',emailD)

with open('failed_emails.csv','w',newline='') as write_obj:
    csv_writer=writer(write_obj)
    csv_writer.writerows([])
with open('emails.csv','w',newline='') as write_obj:
    csv_writer=writer(write_obj)
    csv_writer.writerows([])


with open('urls.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        emailD=[]
        url=row[0]
        # url="http://yogasprites.com"
        process(url)
