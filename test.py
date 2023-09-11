from api_helper import ShoonyaApiPy 
import logging
import pyotp
import datetime
import json
import math
from datetime import date
import time
import csv


#enable dbug to see request and responses 
logging.basicConfig(level=logging.DEBUG)  

#start of our program 
api = ShoonyaApiPy()  

token = '7Y2JE24X452W46K5T7TY6SA54YMHJGN2'

#credentials 
user        = 'FA108285' 
u_pwd       = 'Seema@49' 
vc          = 'FA108285_U' 
app_key     = '14cf02959278b99c7443f4845e9c08b8' 
imei        = 'abc1234'   

ret = api.login(userid=user, password=u_pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei) 

# api.searchscrip('NSE', 'BANKNIFTY')

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

d = date.today()
next_thursday = next_weekday(d, 3) #3 is for thursday
exp_date = next_thursday.strftime("%d%b%y")

def ATM():
        ret = api.get_quotes('NSE', '26009')
        for k,v in ret.items():
            if k == 'lp':
                return round(float(v), -2)

fieldnames = ["x_value"]
            
with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


while True:
    # api.get_security_info('N', '26009')

    strike_price = ATM()

    put_token = ''
    call_token = ''

    put_tokenSearch = api.searchscrip('NFO', 'BANKNIFTY' + exp_date.upper() +'P' + str(int(strike_price)))
    for k,v in put_tokenSearch.items():
        if k == 'values':
            for i in v:
                for x,y in i.items():
                    if x == 'token':
                        put_token = y
            
    call_tokenSearch = api.searchscrip('NFO', 'BANKNIFTY' + exp_date.upper() +'C' + str(int(strike_price)))
    for k,v in call_tokenSearch.items():
        if k == 'values':
            for i in v:
                for x,y in i.items():
                    if x == 'token':
                        call_token = y
                

    # print(put_token)
    # print(call_token)

    call_price = 0
    put_price = 0

    ret = api.get_quotes('NFO', put_token)
    for k,v in ret.items():
            if k == 'lp':
                put_price = v
                # print(k, ": ", v)
                
    ret = api.get_quotes('NFO', call_token)
    for k,v in ret.items():
            if k == 'lp':
                call_price = v
                # print(k, ": ", v)

    sum = float(call_price) + float(put_price)

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {"x_value": str(sum)}
        csv_writer.writerow(info)
    time.sleep(1)


    # api.get_quotes(exchange='NFO', token='')