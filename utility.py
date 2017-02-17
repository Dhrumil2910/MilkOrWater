'''Utility Class used by all 3 Parsers for making a dictionary between date and Stock Price at the closing time on that day
Uses api provied by kibot.com for historical data prices'''
import os
import re
import urllib2

class Utility:
    def __init__(self):
        self.stock_price = ""

    def Make_Stock_Dictionary(self, ticker, ticker_dict, date):
        fo = open("stock_of_Ticker.txt", "w") # Temporary file to store the data
        urllib2.urlopen("http://api.kibot.com/?action=login&user=guest&password=guest") # Authenticate
        string1 = "http://api.kibot.com/?action=history&symbol="
        string2 = ticker
        string3 = "&interval=daily&startdate=1/1/2014&attach=1"
        data =  urllib2.urlopen(string1+string2+string3).read() # Read the URL with the correct ticker
        fo.write(data)
        fo.close()
        fo = open("stock_of_Ticker.txt", "r")
        for line in fo:
            reg = re.findall(r'(\d+\/\d+\/\d+)', line) # Regex to find dates
            reg1 = re.findall(r'\d+\/\d+\/\d+,[\d\.]+,[\d\.]+,[\d\.]+,([\d\.]+),\d+', line) # Regex to extract closing price
            if reg != []:
                ticker_dict[reg[0]] = reg1[0]
        self.stock_price = ticker_dict[date]
        fo.close()
        os.remove("stock_of_Ticker.txt")
