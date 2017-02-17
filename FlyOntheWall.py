# Importing inbuilt modules
import os
import re
import urllib2
import csv
import nltk
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
		self.ticker = []
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
		self.Sector = []
		self.Industry = []
		self.horizon = "12 Months"
		self.SourceLink = ""
		self.PriceTarget = ""
		self.cmp = ""
		self.firm = ""
		self.raw = self.file_pointer.read()
		self.file_pointer.seek(0,0)
		self.data = self.file_pointer.read().replace("\n", "")
		self.file_pointer.seek(0,0)
		self.data = re.sub(r'[^\x00-\x7f]',r' ',self.data)
		self.raw = re.sub(r'[^\x00-\x7f]',r' ',self.raw)

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
			#print link
			if link !=[]:
				self.SourceLink = link[0]
		except Exception, e:
			print str(e)
			
	def MOW(self): # Using self.reco_action and self.reco_type (from the header here) to get reco_action_mow and reco_type_mow
	
		ORIG = orig.Return_ORIG()
		ORIG.rec_type_mow(self.data)
		ORIG.rec_act_mow(self.data)
		self.reco_action = ORIG.reco_action
		self.reco_type = ORIG.reco_type
		
		MOW1 = mow.MOW()
		MOW1.rec_act_mow(self.reco_action)
		self.reco_action_mow = MOW1.reco_action_mow
		#print self.rec_act_mow
		MOW1.rec_type_mow(self.reco_type)
		self.reco_type_mow = MOW1.reco_type_mow
	def Extract_Firm(self):
		try:
			self.firm = re.findall('at\s+(.*)$',self.header)
			#print self.firm
			if self.firm!=[]:
				self.firm = self.firm[0]
		except Exception, e:
			print str(e)
	
	def Extract_Company(self): ### function for etracting the Analyst name using regex and spliting into f_name and l_name
		try:
				tokenised = nltk.word_tokenize(str(self.header))
				tagged = nltk.pos_tag(tokenised)
				for i in tagged:
					if i[0] == 'price':
						break
					if i[1] == 'VBD':
						break
					if i[1] == 'NN':
						break
					else:
						self.Company_Name = self.Company_Name + ' ' + i[0]
				self.Company_Name = self.Company_Name.strip()
				#print self.Company_Name
		
		except Exception, e:
			print str(e)
		
	def Extract_Ticker(self):
		try:
			for index in ['amex.csv', 'nyse.csv', 'nasdaq.csv']:
				with open(index, 'r') as csvfile:
					read_csv = csv.reader(csvfile, delimiter = ',')
					for row in read_csv:
						#print self.Company_Name
						if self.Company_Name.lower() in row[1].lower():
							self.ticker.append(row[0])
							self.Industry.append(row[7])
							self.Sector.append(row[6])
							
			if self.ticker == []:
				self.ticker = ''
			else:
				temp = ''
				count = 0;
				for i in self.ticker:
					if(count == 0):
						temp = temp + i
						count = 1
					else:
						temp = temp + ',' + i
				self.ticker = temp
				
			if self.Industry == []:
				self.Industry = ''
			else:
				temp = ''
				count = 0;
				for i in self.Industry:
					if(count == 0):
						temp = temp + i
						count = 1
					else:
						temp = temp + ',' + i
				self.Industry = temp
				
			if self.Sector == []:
				self.Sector = ''
				
			else:
				temp = ''
				count = 0;
				for i in self.Sector:
					if(count == 0):
						temp = temp + i
						count = 1
						continue
					else:
						temp = temp + ',' + i
				self.Sector = temp
				
			'''if len(self.ticker) == 1:
				self.ticker = self.ticker[0]
			
			if len(self.Industry) == 1:
				self.Industry = self.Industry[0]
				
			if len(self.Sector) == 1:
				self.Sector = self.Sector[0]'''
			
		except Exception, e:
			print str(e)
		
	def Extract_TP(self):
		try:
			dollar = re.findall('\$([0-9]*)',self.data)
			
			if (dollar == []):
				return
			if len(dollar) == 2:
				self.PriceTarget = dollar[0]
			
			if len(dollar) >= 2:
				cent = re.findall('to\s+\$([0-9]*)',self.data)
				if (cent !=[]):
					self.PriceTarget = cent[0]
		
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
		FParser.MOW()
		FParser.Extract_Firm()
		FParser.Extract_Company()
		FParser.Extract_Ticker()
		FParser.Extract_TP()
		FParser.Csv_file_input()
		FParser.file_pointer.close()
	print 'Finish'
	# Write the csv output
	with open('FlyOntheWall.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data)
		
	with open('FlyOntheWall1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('FlyOntheWall2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)
	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))
