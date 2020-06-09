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
        BackSoon.append(str(SoonStock.text[:2]))

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
    #email_to = email_info['info'][2]
    #for testing
    email_to = email_info['info'][0]

    gmail_user = email_address.strip()
    gmail_password = email_pw.strip()
    gmail_to = email_to.strip()

    return gmail_user, gmail_password, gmail_to 


def send_email(gmail_user, gmail_password, gmail_to, subject, OutOfStock, BackSoon, InStock, link):

    ###SENDING EMAIL
    body = 'InStock: ' + str(InStock) +  '<br>' + 'BackSoon: ' + str(BackSoon) +  '<br>' + 'OutofStock: ' + str(OutOfStock) + '<br>' + str(link)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = gmail_to
    msg.attach(MIMEText(str(body), 'html'))
    #msg.attach(MIMEText(str(link), 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_to, msg.as_string())
        server.close()

        print('Email sent!')
    except:
        print ('Something went wrong...')


def checking_stock(link):

    res = requests.get(link, 
    headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})

    zara = bs4.BeautifulSoup(res.text,'lxml')
    
    OutOfStock, BackSoon, InStock = webscrape(zara)
    df = dataframe(OutOfStock, BackSoon, InStock)

    OutOfStock = [item.replace(' ', '') for item in OutOfStock]
    BackSoon = [item.replace(' ', '') for item in BackSoon]
    InStock = [item.replace(' ', '') for item in InStock]

    return OutOfStock, BackSoon, InStock, df


def main():

    link = 'https://www.zara.com/uk/en/knotted-wrap-skirt-p02975878.html?v1=47358279&v2=1445670'

    OutOfStock, BackSoon, InStock, df = checking_stock(link)
    BackSoonSent = ''
    InStockSent = ''
    while 'XS' in OutOfStock or 'XS' in BackSoon or 'XS' in InStock:
        print(df)
        print(datetime.datetime.now())
        if 'XS' in BackSoon and 'True' not in BackSoonSent:
            gmail_user, gmail_password, gmail_to = email_credentials()
            subject = 'ZARA CLOTHES STATUS - BACK SOON'
            BackSoonSent = ['True']
            send_email(gmail_user, gmail_password, gmail_to, subject, OutOfStock, BackSoon, InStock, link)
            continue
        elif 'XS' in InStock and 'True' not in InStockSent:
            gmail_user, gmail_password, gmail_to = email_credentials()
            subject = 'ZARA CLOTHES STATUS - IN STOCK'
            InStockSent = ['True']
            send_email(gmail_user, gmail_password, gmail_to, subject, OutOfStock, BackSoon, InStock, link)
            break
        elif 'XS' in InStock and 'True' in InStockSent:
            break
        else:
            time.sleep(5)
            OutOfStock, BackSoon, InStock, df = checking_stock(link)
            continue



if __name__ == '__main__':
    main()
    

