''' Function Used by Gainers_Today and Benzinga parser for making dictionary b/w Ticker,
Company_Name,Industry and Sector
Not used for briefing.com as its feeds contained no mention of any stock exchange'''
import csv

def make_dict(file_name, dict_name):

    reader = csv.reader(open(file_name)) # File being read from are CSV ,taken from http://www.nasdaq.com/screening/company-list.aspx
    for row in reader:
        key = row[0]
        dict_name[key] = [row[1],row[6],row[7]] # Here row[1] refers to the Company_Name , row[6] refers to Sector , row[7] refers to Industry
amex = {}
nyse = {}
nasdaq = {}

make_dict('amex.csv', amex)
make_dict('nyse.csv', nyse)
make_dict('nasdaq.csv', nasdaq)