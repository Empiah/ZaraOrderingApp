import bs4
import requests
import pandas as pd
import numpy as np
import smtplib

############################################
###THIS PART SCRAPES THE WEB PAGE TO GET DATA FROM ZARA
############################################

res = requests.get('https://www.zara.com/uk/en/knotted-wrap-skirt-p02975878.html?v1=47358279&v2=1445670', 
headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})

zara = bs4.BeautifulSoup(res.text,'lxml')

#Looking for out of stock sizes
OutOfStock = []
for NoStock in zara.find_all('label', attrs={'class':"product-size _product-size disabled _disabled"}):
    OutOfStock.append(str(NoStock.text))

#Looking for sizes labelled as back soon
BackSoon = []
for SoonStock in zara.find_all('label', attrs={'class':"product-size _product-size back-soon _back-soon _disabled"}):
    BackSoon.append(str(SoonStock.text[0]))

#Looking for what is in stock
InStock = []
for Stock in zara.find_all('label', attrs={'class':"product-size _product-size"}):
    InStock.append(str(Stock.text))

#creating dataframe to hold the info
df = pd.DataFrame.from_dict({'OutOfStock': OutOfStock, 'BackSoon': BackSoon, 'InStock':InStock}, orient='index').T
df.fillna(value=np.nan, inplace=True)
df1 = df.replace(np.nan, '', regex=True)

print(df)

############################################
###THIS PART SENDS THE EMAIL
############################################

####################
###GETTING CREDENTIALS
####################

email_info = pd.read_csv('/Users/ophipps/Documents/Apps/OPPythonbot.csv')
email_address = email_info['info'][0]
email_pw = email_info['info'][1]

gmail_user = email_address.strip()
gmail_password = email_pw.strip()

####################
###SENDING EMAIL
####################

sent_from = gmail_user
to = ['oppythonbot@gmail.com']
subject = 'ZARA CLOTHES STATUS'
body = 'OutofStock',OutOfStock,'BackSoon',BackSoon,'InStock',InStock

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print ('Something went wrong...')



