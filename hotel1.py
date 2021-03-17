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
    num = ""
    for i in data:
        encoded = re.findall('mobilesv (.+)\">', str(i))
        num += numbermap[encoded[0]]
    return num


dictionary = {}
page_counter = 1
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
url = "https://www.justdial.com/Delhi/Pure-Veg-Restaurants/nct-10396867/page-"
while page_counter <= 50:
    print("Extracting page "+str(page_counter))
    new_url = url + str(page_counter)
    raw = requests.get(new_url, headers=HEADERS)
    soup = BeautifulSoup(raw.text, 'html5lib')
    boxes = soup.findAll("li", {"class": "cntanr"})
    for counter, data in enumerate(boxes):
        temp = {}
        name = data.findAll("span", {"class": "lng_cont_name"})
        if name:
            temp["name"] = name[0].text
        else:
            temp["name"] = "Unavailabe"
        rating = data.findAll("span", {"class": "green-box"})
        if rating:
            temp["rating"] = rating[0].text
        else:
            temp["rating"] = "Unavailabe"
        votes = data.findAll("span", {"class": "lng_vote"})
        if votes:
            votes[0] = votes[0].text.replace("\n", "")
            temp["votes"] = votes[0].replace("\t", "")
        else:
            temp['votes'] = 'Unavailable'
        number = numberDecoder(data.findAll("span", {"class": "mobilesv"}))
        if number:
            temp["number"] = number
        address = data.findAll("span", {"class": "cont_fl_addr"})
        if address:
            temp["address"] = address[0].text
        else:
            temp["address"] = "Unavailabe"
        p = data.findAll("span", {"class": "distnctxt rsrtopn-1"})
        try:
            if len(p) > 1:
                price = p[0].text
                if " \u20b9" in price:
                    price = price.replace(" \u20b9", "Rs")
                temp['price'] = price
                temp['availablity'] = p[1].text
            else:
                temp['price'] = 'unavailable'
                temp['availablity'] = p[0].text
        except Exception:
            temp['price'] = 'Unavailable'
            temp['availablity'] = 'Unavailable'
        for link in data.findAll('a', {"class": "nlogo lazy srtbyPic"}):
            if link:
                temp["link"] = link['href']
        dictionary[(page_counter-1)*10 + counter+1] = temp
    page_counter += 1
fields = ['Name', 'Phone number', 'address']
with open("hotels.csv", "w", encoding="utf-8") as scribble:
    csvwriter = csv.writer(scribble)
    csvwriter.writerow(fields)
    csvwriter.writerows(dictionary)
print("Written in excel sheet successfully!")
# with open("hotels.json", "w") as writer:
#     writer.write(json.dumps(dictionary, indent=(4)))
