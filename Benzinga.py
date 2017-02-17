# Importing inbuilt modules
import os
import nltk
import re  
import csv
import urllib2

# Local Module imports
import company_info
import divide_files
import date_format
import utility
import mow
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
		self.data = self.file_pointer.read()
		self.data = re.sub(r'[^\x00-\x7f]',r' ',self.data)
		self.data.replace("\n", "")
		self.file_pointer.seek(0,0)

	def Extract_Date(self): # Extracting date from |"Date Sent"| tag in feed
		try:
			for line in self.file_pointer:
				date = re.findall(r'\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M', line)
				if date != []:
					self.date = date[0].split()[0]
					break
			(self.file_pointer).seek(0,0)
		except Exception, e:
			print str(e)
	
	def Extract_Ticker(self):
#Extracting Ticker, Stock Exchange using TICKER:SE expression and then from stock exchanges csv file's
#extracting the company name and its corresponding sector and industry
		try:
			for line in self.file_pointer:
				ticker = re.findall(r'\(.*?>(.*?)</a>\)', line)
				exchange  = re.findall(r'\(([A-Z]+):\s*<a.*?</a>\)', line)
				if exchange != []:
					exchange = exchange[0]
				if ticker!=[]:
					self.ticker = str(ticker[0])
					if exchange == 'NASDAQ':
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
						if self.ticker in company_info.amex.keys():
							self.Company_Name = company_info.amex[ticker[0]][0]
							self.Sector = company_info.amex[ticker[0]][1]
							self.Industry = company_info.amex[ticker[0]][2]
							pass
					else:
						pass
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

	def Extract_SourceLink(self): # Using View article ... <[Link]> expression to extract source link
		try:
			link = re.findall(r'View article\.\.\.\s<(.*?)>', self.data)
			self.SourceLink = link[0]
			
		except Exception, e:
			print str(e)

	def Extract_Analyst(self): ### function for etracting the Analyst name using regex and spliting into f_name and l_name
		try:
			if "analyst" in self.data:
				an = re.findall(r'analyst\s([A-Za-z]+\s[A-Z.]*\s*[A-Za-z]+\s)', self.data)
				se = list(set(an))
			for analyst in se:
				tokenised = nltk.word_tokenize(str(analyst))
				tagged = nltk.pos_tag(tokenised)
				grammar = "NP: {<NNP>+}"
				cp = nltk.RegexpParser(grammar)
				result = cp.parse(tagged)
				reg=re.findall(r'(\(S\s\(NP\s[A-Za-z]+/NNP[A-Za-z]+/NNP\)\))', str(result))
				if "NP" in str(result):
					self.analyst_first_name = analyst.split()[0] 
					self.analyst_last_name = analyst.split()[1]
					
			if self.analyst_last_name.endswith('.'):
				self.analyst_first_name = self.analyst_first_name + ' ' + self.analyst_last_name
				self.analyst_last_name = analyst.split()[2]


		except Exception, e:
			print str(e)

	
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

	def Output_of_RecoAction_orig_and_RecoType_orig(self): ### function calling the function for extracting the RecoAction and RecoType
		try:
			self.Get_the_RecoAction_origmow_and_RecoType_origmow(self.ticker, self.date)

		except Exception, e:
			print str(e)


	def Get_the_RecoAction_origmow_and_RecoType_origmow(self, Ticker, Ticker_Date): ### Extracting the RecoAction and RecoType using regex
		self.Make_file_for_source_code(Ticker)
		with open("RecoAction_orig.txt", "r") as fo:
			data= fo.read().replace("\n", "")
		reg = re.findall(r'<tbody.*?>(.*?)</tbody>', data)
		reg1 = re.findall(r'<tr.*?>(.*?)</tr>', str(reg[0]))
		for li in reg1:
			row = re.findall(r'<td.*?>(.*?)</td>', li)
			date_format_change = date_format.convert_date(row[0])
			date_format_change.convert_into_a_specific_format()
			date_changed =  date_format_change.final
			count = 0
			if date_changed in Ticker_Date or Ticker_Date in date_changed:

				if row[1] != "":
					splited_firm_name = row[1].split()
					length = len(splited_firm_name)
					for i in xrange(length):
						if splited_firm_name[i] in self.data:
							count=count+1
					if count != 0:
						self.firm = row[1]
						self.reco_type = row[2]
						self.reco_action = row[4]
						self.PriceTarget = row[5]
						break
		# Using self.reco_action and self.reco_type to get reco_action_mow and reco_type_mow
		MOW1 = mow.MOW()   ### Might want to change this  
		MOW1.rec_act_mow(self.reco_action)  
		MOW1.rec_type_mow(self.reco_type)
		self.reco_action_mow = MOW1.reco_action_mow
		self.reco_type_mow =  MOW1.reco_type_mow
		fo.close()
	
	def Make_file_for_source_code(self, Ticker): ### storing the source code of the website into a file named "RecoAction_orig.txt" 
		fo = open("RecoAction_orig.txt", "w")
		string1 = "http://www.benzinga.com/stock/"
		string2 = Ticker
		string3 = "/ratings"
		source_code = urllib2.urlopen(string1 + string2 + string3).read()
		fo.write(source_code)
		fo.close()  
		
if __name__ == "__main__":
	# Start the controller
	filename = raw_input("Enter the Filename you want to parse: ")
	make_files = divide_files.MakeFiles(filename) ## dividing the input file into multiple files
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
		FParser.Extract_Headline()
		FParser.Extract_SourceLink()
		FParser.Extract_Analyst()
		FParser.Output_of_RecoAction_orig_and_RecoType_orig()
		FParser.Csv_file_input()
		FParser.file_pointer.close()
		
	print 'Finish'

	with open('benzinga.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter = ',')
		csv_write.writerows(Csv_Data)
		
	with open('benzinga1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('benzinga2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)
	
	# Removing Temporary Files
	try:
		os.remove("RecoAction_orig.txt")

	except Exception, e:
			print str(e)
	
	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))