# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 14:37:23 2020

@author: Meet Hariya
"""


from bs4 import BeautifulSoup
import requests
import re
import csv

numbermap = {
             'icon-dc': '+',
             'icon-fe': '(',
             'icon-hg': ')',
             'icon-ba': '-',
             'icon-ji': '9',
             'icon-lk': '8',
             'icon-nm': '7',
             'icon-po': '6',
             'icon-rq': '5',
             'icon-ts': '4',
             'icon-vu': '3',
             'icon-wx': '2',
             'icon-yz': '1',
             'icon-acb': '0'
             }


def numberDecoder(data):
    num = '"'
    for i in data:
        encoded = re.findall('mobilesv (.+)\">', str(i))
        num += numbermap[encoded[0]]
    num += '"'
    return num


dictionary = []
page_counter = 1
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
url = "https://www.justdial.com/Delhi/Pure-Veg-Restaurants/nct-10396867/page-"
while page_counter <= 50:
    new_url = url + str(page_counter)
    print("Connecting to page", page_counter)
    raw = requests.get(new_url, headers=HEADERS)
    soup = BeautifulSoup(raw.text, 'html5lib')
    boxes = soup.findAll("li", {"class": "cntanr"})
    for data in boxes:
        temp = []
        name = data.findAll("span", {"class": "lng_cont_name"})
        if name:
            temp.append(name[0].text)
        else:
            temp.append("Unavailabe")
        number = numberDecoder(data.findAll("span", {"class": "mobilesv"}))
        if number:
            temp.append(number)
        address = data.findAll("span", {"class": "cont_fl_addr"})
        if address:
            temp.append(address[0].text)
        else:
            temp.append("Unavailabe")
        dictionary.append(temp)
    print("Page ", page_counter, "Extracted")
    page_counter += 1
fields = ['Name', 'Phone number', 'address']
print("Writting in excel sheet....Please wait")
with open("hotels.csv", "w", encoding="utf-8") as scribble:
    csvwriter = csv.writer(scribble)
    csvwriter.writerow(fields)
    csvwriter.writerows(dictionary)
print("Written in excel sheet successfully!")
