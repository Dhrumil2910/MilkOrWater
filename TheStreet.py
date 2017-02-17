# Importing inbuilt modules
import os
import re
import urllib2
import csv
from bs4 import BeautifulSoup

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

def zhukov(original):    # Here Original is rss feed headline string
		original = original.lower()
		temp = []
		if "downgrade" in original:
			temp.append("Downgrade")
		
		if "upgrade" in original:
			temp.append("Upgrade")
		
		if "reiterate" in original:
			temp.append("Reiterate")
			
		if "initiate" in original:
			temp.append("Initiate")
		
		if 'lower' in original and 'estimate' in original:
			temp.append('Lower Estimate')
		
		if 'cut' in original and 'estimate' in original:
			temp.append('Estimate Cut')
			
		if 'boost' in original and 'estimate' in original:
			temp.append('Boost Estimate')
		
		if 'raise' in original and 'estimate' in original:
			temp.append('Raise Estimate')
		
		if 'lower' in original and ("price" and "target")  in original:
			temp.append('Price Target Lowered')
		
		if 'cut' in original  and ("price" and "target") in original:
			temp.append('Price Target Cut')
		
		if 'boost' in original and ("price" and "target") in original:
			temp.append('Price Target Boosted')
		
		if 'raise' in original and ("price" and "target") in original:
			temp.append('Price Target Raised')
		
		if 'lift' in original and ("price" and "target") in original:
			temp.append('Price Target Raised')
		
		if 'move' in original and ("price" and "target") in original:
			temp.append('Price Target Changed')
			
		return temp
			

def popov(original): # Original is rss feed headline string
		original = original.lower()
		temp = []
	
		if "positive" in original: # Buy Cases
			temp.append("Positive")
		
		if "add" in original:
			temp.append("Add")
		
		if "accumulate" in original:
			temp.append("Accumulate")
		
		if "buy"  in original:
			temp.append("Buy")
			
		if ("top" or "best") in original and ("pick") in original:
			temp.append("Top Pick")
			
		if ("out") in original and ("perform") in original:
			temp.append("Out Perform")
			
		if ("over") in original and ("weight") in original:
			temp.append("Over Weight")
			
		if ("above") in original and ("average") in original:
			temp.append("Above Average")
		
		if("under") in original and ("weight") in original: # Sell Cases
			temp.append("Under Weight")
			
		if("under") in original and ("perform") in original:
			temp.append("Under Perform")
				
		if "reduce" in original:
			temp.append("Reduce")
			
		if "sell" in original:
			temp.append("Sell")
														
		if "hold" in original: # Hold Cases
			temp.append("Hold")
			
		if "average" in original:
			temp.append("Average")
			
		if "perform" in original:
			temp.append("Perform")
			
		if "neutral" in original:
			temp.append("Neutral")
		
		if("equal") in original and ("weight") in original:
			temp.append("Equal Weight")
			
		if("in") in original  and ("line") in original:
			temp.append("In Line")

		return temp

			
class FeedsParser(Backbone): # Initializing the fields and changing the rss feed to a single line
	def __init__(self, filename):
		Backbone.__init__(self)
		self.filename = filename
		self.file_pointer = open(self.filename, "r")
		self.ticker = []
		self.date = ""
		self.dict = {}
		self.analyst_first_name = "Research"
		self.analyst_last_name = "Analyst"
		self.reco_action_mow = []
		self.reco_type_mow = []
		self.reco_action = []
		self.reco_type = []
		self.Company_Name = []
		self.header = ""
		self.Sector = []
		self.Industry = []
		self.horizon = "12 Months"
		self.SourceLink = ""
		self.PriceTarget = []
		self.cmp = []
		self.firm = []
		self.raw = self.file_pointer.read()
		self.file_pointer.seek(0,0)
		self.data = self.file_pointer.read().replace("\n", "")
		self.file_pointer.seek(0,0)
		self.raw = re.sub(r'[^\x00-\x7f]',r' ',self.raw)
		self.data = re.sub(r'[^\x00-\x7f]',r' ',self.data)
		self.flag = 0
		self.soup = ''
		self.lifeline = ''

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
			
	def Extract_Ticker(self):
		try:
			if (self.flag == 1):
				temp = re.findall('\((\S*)\)',self.data)
				for i in temp:
					self.ticker.append(i)
			
			else:
				data = re.findall('<strong>.*</strong>\s<span class="TICKERFLAT">.*</span>.*',self.data)
				for i in data:
					temp = i
					temp = BeautifulSoup(temp)
					self.ticker.append(temp.find('a').get_text())
					
		except Exception, e:
			print str(e)
	def Extract_Firm(self):
		try:
			if self.flag == 1:
				data = re.findall('from\s+([A-Za-z-,.]*)',self.data)
				for i in data:
					self.firm.append(i)
				
				while len(self.firm) < len(self.ticker):
					self.firm.append('')
					
			else:
				data = re.findall('<strong>.*</strong>\s<span class="TICKERFLAT">.*</span>.*',self.data)
				for i in data:
					temp = i
					temp = BeautifulSoup(temp).get_text()
					string = re.findall('at\s+(\S*\s+\S*)',temp)
					if string != []:
						self.firm.append(string[0])
					else:
						self.firm.append('')
						
		except Exception, e:
			print str(e)				
	def Extract_Company_Industry_Sector(self): # Using company TICKER to search in the three main stock exchanges for company name and its sector and industry
		try:
			for i in self.ticker:
				for index in ['amex.csv', 'nyse.csv', 'nasdaq.csv']:
					with open(index, 'r') as csvfile:
						read_csv = csv.reader(csvfile, delimiter = ',')
						for row in read_csv:
							if i == row[0]:
								self.Company_Name.append(row[1])
								self.Industry.append(row[7])
								self.Sector.append(row[6])
								break
			
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
			for i in self.ticker:
				
				#print self.date
				Utility1 = utility.Utility()
				if i!='':
					Utility1.Make_Stock_Dictionary(i, self.dict, self.date)
					self.cmp.append(Utility1.stock_price)
				else:
					self.cmp.append('')
		except Exception, e:
			print str(e)
				
	def MOW(self): # Using self.reco_action and self.reco_type (from the header here) to get reco_action_mow and reco_type_mow
		try:
			if self.flag!=1: # Change code to that to be used in a list
					data = re.findall('<strong>.*</strong>\s<span class="TICKERFLAT">.*</span>.*',self.data)
					for i in data:
						temp = i
						temp = BeautifulSoup(temp).get_text()
						ORIG = orig.Return_ORIG()
						ORIG.rec_type_mow(temp)
						ORIG.rec_act_mow(temp)
						self.reco_action.append(ORIG.reco_action)
						self.reco_type.append(ORIG.reco_type)
						
						MOW1 = mow.MOW()
						MOW1.rec_act_mow(ORIG.reco_action)
						MOW1.rec_type_mow(ORIG.reco_type)
						self.reco_type_mow.append(MOW1.reco_type_mow)
						self.reco_action_mow.append(MOW1.reco_action_mow)
						
			else:
				reco_action = popov(self.data)
				reco_type = zhukov(self.data)
				mow_type = []
				mow_action = []
				
				for i in reco_action:
					self.reco_action.append(i)
					MOW1 = mow.MOW()
					MOW1.rec_act_mow(i)
					self.reco_action_mow.append(MOW1.reco_action_mow)
					
				for i in reco_type:
					self.reco_type.append(i)
					MOW1 = mow.MOW()
					MOW1.rec_type_mow(i)
					self.reco_type_mow.append(MOW1.reco_type_mow)
					
				while len(self.reco_type) < len(self.ticker):
					self.reco_type.append('')
					
				while len(self.reco_action) < len(self.ticker):
					self.reco_action.append('')
					
				while len(self.reco_type_mow) < len(self.ticker):
					self.reco_type_mow.append('')
					
				while len(self.reco_action_mow) < len(self.ticker):
					self.reco_action_mow.append('')
		
		except Exception, e:
			print str(e)
	def Extract_TP(self):
		try:
			if self.flag == 1:
				action = re.findall('to\s+\$([0-9]*)',self.data)
				action2 = re.findall('is\s+\$([0-9]*)',self.data)
				action3 = re.findall('\s+\$([0-9]*)',self.data)
				for i in action:
					self.PriceTarget.append(i)
				
				for i in action2:
					self.PriceTarget.append(i)
					
				if len(self.PriceTarget) < len(self.ticker):
					for i in action2:
						self.PriceTarget.append(i)
					
				while len(self.PriceTarget) < len(self.ticker):
					self.ticker.PriceTarget('')
					
			else:
				data = re.findall('<strong>.*</strong>\s<span class="TICKERFLAT">.*</span>.*',self.data)
				for i in data:
						temp = i
						temp = BeautifulSoup(temp).get_text()
						
						string = re.findall('is\s+\$([0-9]*)',temp)
						#print temp
						if string != []:
							self.PriceTarget.append(string[0])
						else:
							string = re.findall('to\s+\$([0-9]*)',temp)
							if string!=[]:
								self.PriceTarget.append(string[0])
							else:
								string = re.findall('\s+\$([0-9]*)',temp)
								if string!=[]:
									self.PriceTarget.append(string[0])
								else:
									self.PriceTarget.append('')
									
		except Exception, e:
			print str(e)
		
	def Make_file_for_source_code(self): ### storing the source code of the website into a file named "RecoAction_orig.txt" 
		#fo = open("RecoAction_orig.txt", "w")
		source_code = urllib2.urlopen(self.SourceLink).read()
		self.soup = source_code
		self.soup = BeautifulSoup(self.soup)
		if '/video/' in self.SourceLink:
			self.flag = 1
		
		if self.flag == 1:
			self.data = self.soup.find('div', {'id':'currentDescription'}).get_text()
		
		else:
			self.data = str(self.soup.find('div',{'class':'virtualpage'}))
			
		
	def Csv_file_input(self): ## Every time appending the all the columns extracted from the RSS Feeds into the CSV file.
		try:
			for i in range(0,len(self.ticker)): 
				Csv_Data.append([self.date, self.Company_Name[i], self.ticker[i], self.firm[i], self.reco_action[i], \
				self.reco_action_mow[i], self.cmp[i], self.PriceTarget[i], \
				self.horizon, self.analyst_first_name, self.analyst_last_name, \
				self.analyst_email, self.analyst_tc, self.Sector[i], \
				self.Industry[i], self.header, self.notes, self.reco_type[i], \
				self.reco_type_mow[i], self.SourceLink, self.status, self.curated, self.raw])
				
				Csv_Data1.append([self.firm[i]])
			
				Csv_Data2.append([self.Company_Name[i], self.firm[i]])
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
		FParser.Extract_SourceLink()
		FParser.Extract_Headline()
		FParser.Make_file_for_source_code()
		FParser.Extract_Ticker()
		FParser.Extract_Firm()
		FParser.Extract_Company_Industry_Sector()
		FParser.MOW()
		FParser.Extract_Stock_Price()
		FParser.Extract_TP()
		FParser.Csv_file_input()
		FParser.Make_file_for_source_code()
		FParser.file_pointer.close()
	
	print 'Finish'
	# Write the csv output
	with open('TheStreet.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data)
		
	with open('TheStreet1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('TheStreet2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)
	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))