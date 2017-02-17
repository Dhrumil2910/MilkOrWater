# Importing inbuilt modules
import os
import re
import urllib2
import csv
from bs4 import BeautifulSoup

# Local Module imports
import divide_files
import utility
import mow
from common import Backbone
from common import Csv_Data
from common import Csv_Data1
from common import Csv_Data2

# No data is present in the text file except for a single line, PRICE TARGET is given only on the website for the corresponding feed

class FeedsParser(Backbone):  # Initializing the fields and changing the rss feed to a single line
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
		self.data =  re.sub(r'[^\x00-\x7f]',r' ',self.data)
		self.file_pointer.seek(0,0)

	def Extract_Firmname(self): # Extracting firm name using expression <td>ISI Group issues 
		try:
			for line in self.file_pointer:
				firm = re.findall(r'<td>\s*(.*?)\s*issues', line)
				if firm != []:
					self.firm = firm[0]
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
									
	def Extract_Date(self): # Extracting date from |"Date Sent"| tag in feed
		try:
			for line in self.file_pointer:
				date = re.findall(r'\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M', line)
				if date != []:
					self.date = date[0].split()[0]
					break
			self.file_pointer.seek(0,0)			
		except Exception, e:
			print str(e)
					
	def Extract_Ticker(self): # Extracting TICKER using expression "|"ANET:
		try:
			for line in self.file_pointer:
				ticker = re.findall(r'[A-Z]+:', line)\
				
				if ticker != []:
					self.ticker = ticker[0][:-1]
			self.file_pointer.seek(0,0)
		
		except Exception, e:
			print str(e)

	def Extract_SourceLink(self): # Using View article ... <[Link]> expression to extract source link
		try:
			link = re.findall(r'View article\.\.\.\s<(.*?)>', self.data)
			self.SourceLink = link[0]
		
		except Exception, e:
			print str(e)
			
	def Extract_Headline(self): # Using --> ANET: ISI Group reits Strong Buy"|  <-- expression to extract source link
		try:
			for line in self.file_pointer:
				header = re.findall(r'[A-Z]+: .+\|', line)
				if header != []:
					self.header = header[0][:-1]
					self.header = self.header[:-1]
			self.file_pointer.seek(0,0)
			
		except Exception, e:
			print str(e)
		
	def Extract_Company_Industry_Sector(self): # Using company TICKER to search in the three main stock exchanges for company name and its sector and industry
		try:
			for index in ['amex.csv', 'nyse.csv', 'nasdaq.csv']:
				with open(index, 'r') as csvfile:
					read_csv = csv.reader(csvfile, delimiter = ',')
					for row in read_csv:
						if self.ticker == row[0]:
							self.Company_Name = row[1]
							self.Industry = row[7]
							self.Sector = row[6]
							break
			
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
			
	def Make_file_for_source_code(self): ### storing the source code of the website into a file named "RecoAction_orig.txt" 
		fo = open("RecoAction_orig.txt", "w")
		source_code = urllib2.urlopen(self.SourceLink).read()
		fo.write(source_code)
		fo.close()
	
	def Extract_Action_Type_Target(self): # Using Beautiful Soup we extract the data from the source link
		fo = open("RecoAction_orig.txt", "r")
		soup = BeautifulSoup(fo)
		table = soup.find('tr', {'class': 'wh-row'}) # we find self.reco_action , self.PriceTarget in the children of tr tag having class = 'wh-row'
		type  = soup.find('span', {'class': 'row-title'}) # we find reco_type in span tag class ='row-title'
		count = 0
		self.reco_type = type.text
		for i in table.findAll("td"):
			count += 1
			if count == 4:
				self.reco_action = i.text

			if count == 5:
				PriceTarget = i.text

		self.PriceTarget = re.findall(r'\s+\$([0-9]+)', PriceTarget)
		if len(self.PriceTarget) == 0:
			self.PriceTarget = re.findall(r'\$([0-9]+)', PriceTarget)
		self.PriceTarget = self.PriceTarget[0]

	def MOW(self): # Using self.reco_action and self.reco_type to get reco_action_mow and reco_type_mow
		MOW1 = mow.MOW()
		MOW1.rec_act_mow(self.reco_action)
		self.reco_action_mow = MOW1.reco_action_mow
		MOW1.rec_type_mow(self.reco_type)
		self.reco_type_mow = MOW1.reco_type_mow
			
if __name__ == "__main__":
	# Start the controller
	filename = raw_input("Enter the Filename you want to parse: ")
	make_files = divide_files.MakeFiles(filename)   ## dividing the input file into multiple files
	make_files.divide_into_files()
	files = make_files.count_files/2    ## counting the number of the *.1 files

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
		FParser.Extract_Company_Industry_Sector()    
		FParser.Extract_Firmname()      
		FParser.Make_file_for_source_code()   
		FParser.Extract_Action_Type_Target()    
		FParser.MOW()
		FParser.Csv_file_input()
		FParser.file_pointer.close()
		
	print 'Finish'
		
	# Create instances of Feed Parser class  
	with open('briefing.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter = ',')
		csv_write.writerows(Csv_Data)
		
	with open('briefing1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('briefing2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)

	# Removing Temporary Files  
	os.remove("RecoAction_orig.txt")

	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))
	
