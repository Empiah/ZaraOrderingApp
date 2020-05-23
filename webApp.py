import bs4 
from selenium import webdriver 
import requests
import json
import re

res = requests.get('https://www.zara.com/uk/en/knotted-wrap-skirt-p02975878.html?v1=47358279&v2=1445670', 
headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})

zara = bs4.BeautifulSoup(res.text,'lxml')


#OutOfStock = zara.find_all('label', attrs={'class':"product-size _product-size disabled _disabled"})
print('---------------','\nOut of Stock','\n---------------')

for OutOfStock in zara.find_all('label', attrs={'class':"product-size _product-size disabled _disabled"}):
    print(OutOfStock.text)

print('---------------','\nBack Soon','\n---------------')

for BackSoon in zara.find_all('label', attrs={'class':"product-size _product-size back-soon _back-soon _disabled"}):
    print(BackSoon.text[0])

print('---------------','\nIn Stock','\n---------------')

for InStock in zara.find_all('label', attrs={'class':"product-size _product-size"}):
    print(InStock.text)






