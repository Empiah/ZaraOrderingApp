#TODO
#loop every x amount of time to check
#only send email when status changes for XS or S size


import bs4
import requests
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime

def webscrape(zara):
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

    return OutOfStock, BackSoon, InStock

def dataframe(OutOfStock, BackSoon, InStock):
    #creating dataframe to hold the info
    df = pd.DataFrame.from_dict({'OutOfStock': OutOfStock, 'BackSoon': BackSoon, 'InStock':InStock}, orient='index').T
    df.fillna(value=np.nan, inplace=True)
    #df1 = df.replace(np.nan, '', regex=True)

    return df

def email_credentials():
    email_info = pd.read_csv('/Users/ophipps/Documents/Apps/OPPythonbot.csv')
    email_address = email_info['info'][0]
    email_pw = email_info['info'][1]
    email_to = email_info['info'][2]

    gmail_user = email_address.strip()
    gmail_password = email_pw.strip()
    gmail_to= email_to.strip()

    return gmail_user, gmail_password, gmail_to 


def send_email(gmail_user, gmail_password, gmail_to, OutOfStock, BackSoon, InStock, link):

    ###SENDING EMAIL
    sent_from = gmail_user
    to = gmail_to
    subject = 'ZARA CLOTHES STATUS'
    body = 'InStock: ' + str(InStock) +  '<br>' + 'BackSoon: ' + str(BackSoon) +  '<br>' + 'OutofStock: ' + str(OutOfStock) + '<br>' + str(link)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = to
    msg.attach(MIMEText(str(body), 'html'))
    #msg.attach(MIMEText(str(link), 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()

        print('Email sent!')
    except:
        print ('Something went wrong...')


def checking_stock():

    link = 'https://www.zara.com/uk/en/knotted-wrap-skirt-p02975878.html?v1=47358279&v2=1445670'

    res = requests.get(link, 
    headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})

    zara = bs4.BeautifulSoup(res.text,'lxml')
    
    OutOfStock, BackSoon, InStock = webscrape(zara)
    df = dataframe(OutOfStock, BackSoon, InStock)

    return OutOfStock, BackSoon, InStock, df, link


def main():

    
    OutOfStock, BackSoon, InStock, df, link = checking_stock()
    print(OutOfStock, BackSoon, InStock)
    while 'XS ' in OutOfStock:
        print(df)
        print(datetime.datetime.now())
        if 'XS ' in InStock:
            gmail_user, gmail_password, gmail_to = email_credentials()
            send_email(gmail_user, gmail_password, gmail_to, OutOfStock, BackSoon, InStock, link)
            break
        else:
            time.sleep(5)
            OutOfStock, BackSoon, InStock, df, link = checking_stock()
            continue


if __name__ == '__main__':
    main()
    

