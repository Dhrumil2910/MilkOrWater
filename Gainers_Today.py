# Importing inbuilt modules
import os
import re
import urllib2
import csv

# Local Module imports
import company_info
import divide_files
import date_format
import utility
import mow
import orig
from common import Backbone
from common import Csv_Data
from common import Csv_Data1
from common import Csv_Data2

class FeedsParser(Backbone): # Initializing the fields and changing the rss feed to a single line
	def __init__(self, filename):
		Backbone.__init__(self)
		self.filename = filename
		self.file_pointer = open(self.filename, "r")		
		self.ticker = ""
		self.date = ""
		self.dict = {}
		self.analyst_first_name = "Research"
		self.analyst_last_name = "Analyst"
		self.reco_action_mow = " "
		self.reco_type_mow = " "
		self.reco_action = " "
		self.reco_type = " "
		self.Company_Name = ""
		self.header = ""
		self.Sector = ""
		self.Industry = ""
		self.horizon = "12 Months"
		self.SourceLink = ""
		self.PriceTarget = ""
		self.cmp = ""
		self.firm = ""
		self.raw = self.file_pointer.read()
		self.raw = re.sub(r'[^\x00-\x7f]',r' ',self.raw)
		self.file_pointer.seek(0,0)
		self.data = self.file_pointer.read().replace("\n", "")
		self.data = re.sub(r'[^\x00-\x7f]',r' ',self.data)
		self.file_pointer.seek(0,0)

	def Extract_Date(self): # Extracting date from 'Rated Date'
		try:
			for line in self.file_pointer:
				date = re.findall(r'Rated Date:\s*(\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M)', line)
				if date != []:
					self.date = date[0].split()[0]
					break
			self.file_pointer.seek(0,0)      
		except Exception, e:
			print str(e)

	def Extract_Ticker(self): 
#Extracting Ticker, Stock Exchange using TICKER:SE expression and then from stock exchanges csv file's
#extracting the company name and its corresponding sector and industry
		try:
			#fp = open(self.filename, "r")
			for line in self.file_pointer:
				ticker = re.findall(r'\([A-Z]*\s*:\s*([A-Z]*)\)', line)
				exchange = re.findall(r'\(([A-Z]*)\s*:\s*[A-Z]*\)', line)
				
				if ticker != [] and exchange != []:
					exchange = exchange[0]
					self.ticker = str(ticker[0])
					if(exchange == 'NASDAQ'):
						if ticker[0] in company_info.nasdaq.keys():
							self.Company_Name = company_info.nasdaq[ticker[0]][0]
							self.Sector = company_info.nasdaq[ticker[0]][1]
							self.Industry = company_info.nasdaq[ticker[0]][2]
							pass
					elif exchange == "NYSE":
						if self.ticker in company_info.nyse.keys():
							self.Company_Name = company_info.nyse[ticker[0]][0]
							self.Sector = company_info.nyse[ticker[0]][1]
							self.Industry = company_info.nyse[ticker[0]][2]
							pass
					elif exchange == "AMEX":
						if(self.ticker in company_info.amex.keys()):
							self.Company_Name = company_info.amex[ticker[0]][0]
							self.Sector = company_info.amex[ticker[0]][1]
							self.Industry = company_info.amex[ticker[0]][2]
							pass
					else:
						pass
					break
			self.file_pointer.seek(0,0)          
		except Exception, e:
			print str(e)

	def Extract_Stock_Price(self): # Converting dates of form 1/##/** to 01/##/** and using kibot api for obtaining historical stock prices
		try:
			date_split = self.date.split('/')
			if int(date_split[0]) < 10:
				date_split[0] = '0' + date_split[0]
			if int(date_split[1]) < 10:
				date_split[1] = '0' + date_split[1]
			self.date = date_split[0] + '/' + date_split[1] + '/' + date_split[2]
			Utility1 = utility.Utility()
			Utility1.Make_Stock_Dictionary(self.ticker, self.dict, self.date)
			self.cmp = Utility1.stock_price
		except Exception, e:
			print str(e)

	def Extract_Headline(self): ## Extracting Headline using regex involving the pattern --> 8/28/2014 5:55:00 PM"|"Head Line"|" 
		try:
			header = re.findall(r'\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M\"\|\"(.*?)\"\|\"', self.data)
			self.header = header[0]
		except Exception, e:
			print str(e)
	
	def Extract_TP(self): # Extracting the target price from headline  
		try:
			target_price = re.findall(r'price target\s+\$([0-9]+)', self.header)
			if len(target_price) != 0:
				self.PriceTarget = target_price[0]
		except Exception, e:
			print str(e)
			
	def Extract_Firm(self): # Using |'Firm Name Co.'| expression for extracting firm name 
			firm = re.findall(r'(\|\"([A-Z][A-Za-z,./$&?]*\s)*[A-Z][A-Za-z,./$&?]+\"\|\|)', self.data)
			firm = firm[0][0]
			firm = firm[:-1]
			firm = firm[:-1]
			firm = firm[:-1]
			firm = firm[1:]
			firm = firm[1:]
			self.firm = firm
		
	def Extract_SourceLink(self): # Using View article ... <[Link]> expression to extract source link
		try:
			link = re.findall(r'View article\.\.\.\s<(.*?)>', self.data)
			self.SourceLink = link[0]
			
		except Exception, e:
			print str(e)
	
	def MOW(self): # Using self.reco_action and self.reco_type to get reco_action_mow and reco_type_mow
		MOW1 = mow.MOW()
		MOW1.rec_act_mow(self.header)
		self.reco_action_mow = MOW1.reco_action_mow
		MOW1.rec_type_mow(self.header)
		self.reco_type_mow = MOW1.reco_type_mow
		ORIG = orig.Return_ORIG()
		ORIG.rec_act_mow(self.header)
		ORIG.rec_type_mow(self.header)
		self.reco_action = ORIG.reco_action  
		self.reco_type = ORIG.reco_type 
	
	def Csv_file_input(self): ## Every time appending the all the columns extracted from the RSS Feeds into the CSV file.
		try:
			Csv_Data.append([self.date, self.Company_Name, self.ticker, self.firm, self.reco_action, \
				self.reco_action_mow, self.cmp, self.PriceTarget, \
				self.horizon, self.analyst_first_name, self.analyst_last_name, \
				self.analyst_email, self.analyst_tc, self.Sector, \
				self.Industry, self.header, self.notes, self.reco_type, \
				self.reco_type_mow, self.SourceLink, self.status, self.curated, self.raw])
				
			Csv_Data1.append([self.firm])
			
			Csv_Data2.append([self.Company_Name, self.firm])
			
		except Exception, e:
			print str(e)
			
if __name__ == '__main__':
	# Start the controller 
	filename = raw_input("Enter the Filename you want to parse: ") ## dividing the input file into multiple files
	make_files = divide_files.MakeFiles(filename)
	make_files.divide_into_files()
	files = make_files.count_files/2 ## counting the number of the *.1 files
	
	# Create instances of Feed Parser class 
	for i in xrange(files):
		print "Total Complete " + str(i*100/files) + '%'
		index = str(i+2) + ".1"
		FParser = FeedsParser(index)
		FParser.Extract_Date()
		FParser.Extract_Ticker()
		FParser.Extract_Stock_Price()
		FParser.Extract_SourceLink()
		FParser.Extract_Headline()
		FParser.Extract_TP()
		FParser.Extract_Firm()
		FParser.MOW()
		FParser.Csv_file_input()
		FParser.file_pointer.close()
	
	
	print 'Finish'
	# Write the csv output
	with open('gainers_today.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data)
		
	with open('gainers_today1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('gainers_today2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)
	
	# Removing Temporary Files
	#os.remove("RecoAction_orig.txt") We Don't access the website to get the data
	
	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))
