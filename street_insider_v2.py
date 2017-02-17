# Importing inbuilt modules
import os
import re
import urllib2
import nltk
import csv

# Local Module imports
import company_info
import divide_files
import date_format
import utility
import mow
import orig
from bs4 import BeautifulSoup
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
		self.reco_action_mow = []
		self.reco_type_mow = []
		self.reco_action = []
		self.reco_type = []
		self.Company_Name = []
		self.header = []
		self.Sector = []
		self.Industry = []
		self.horizon = "12 Months"
		self.SourceLink = ""
		self.PriceTarget = []
		self.cmp = []
		self.firm = []
		self.raw = self.file_pointer.read()
		self.raw = re.sub(r'[^\x00-\x7f]',r' ',self.raw)
		self.file_pointer.seek(0,0)
		self.data = self.file_pointer.read().replace("\n", "")
		self.data = re.sub(r'[^\x00-\x7f]',r' ',self.data)
		self.file_pointer.seek(0,0)
		self.html = BeautifulSoup(re.findall(r'\"(<html>.*</html>)\"',self.data)[0])
		self.ptag = self.html.findAll('p',{'class':''})
		
	def Filter_Feeds(self): ## Extracting Headline using regex involving the pattern --> 8/28/2014 5:55:00 PM"|"Head Line"|"
		try:
			header = re.findall(r'\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M\"\|\"(.*?)\"\|\"', self.data)
			if "analyst rating".lower() in header[0].lower():
				return True
			else:
				return False
		except Exception, e:
			print str(e)

	def Extract_Date(self):
		try:
			for line in self.file_pointer:
				date = re.findall(r'\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M', line)
				if date != []:
					self.date = date[0].split()[0]
				break
			self.file_pointer.seek(0,0)			
		except Exception, e:
			print str(e)
	
	def Extract_SourceLink(self): # Using View article ... <[Link]> expression to extract source link
		try:
			link = re.findall(r'View article\.\.\.\s<(.*?)>', self.data)
			self.SourceLink = link[0]
		except Exception, e:
			print str(e)
	
	def Clean_Ptags(self):
		try:
			for i in self.ptag:
				if(i.a!=None):
					i.a.decompose()
				if(i.strong!=None):
					i.strong.decompose()
				# Remove the unnecessary nodes in the list
				popper = []
				for i in range(0,len(self.ptag)):
					#print str(i)
					if ":" in self.ptag[i].get_text():
						continue
					else:
						popper.append(self.ptag[i])
				for i in popper:
					self.ptag.remove(i)
		except Exception, e:
			print str(e)
			
	def Extract_TP(self):
		try:
			for i in self.ptag:
				string  = 'to\s+\$([0-9]*.?[0-9]+)'
				string2 = 'of\s+\$([0-9]*.?[0-9]+)'
				gamma = re.findall(string,i.get_text()) # gamma === Target Price
				if gamma == []:
					gamma = re.findall(string2,i.get_text())
				if(gamma == []):
					self.PriceTarget.append('')
				else:
					self.PriceTarget.append(gamma[0])		
		except Exception, e:
			print str(e)
			
	def Extract_Ticker(self):
			try:
				for i in self.ptag:
					string = ':\s+([A-Za-z]*)\)'
					string2 = '\(([A-Za-z]*): '
					ticker = re.findall(string,i.get_text())
					if(ticker==[]):
						ticker=['']
					self.ticker.append(ticker[0])
					exchange = re.findall(string2,i.get_text())
					if(exchange==[]):
						exchange=''
					else:
						exchange = exchange[0]
					if ticker[0] != '' and exchange != '':
						if(exchange.lower() == 'nasdaq'):
							if ticker[0] in company_info.nasdaq.keys():
								self.Company_Name.append(company_info.nasdaq[ticker[0]][0])
								self.Sector.append(company_info.nasdaq[ticker[0]][1])
								self.Industry.append(company_info.nasdaq[ticker[0]][2])
			
						elif exchange.lower() == "nyse":
							if ticker[0] in company_info.nyse.keys():
								self.Company_Name.append(company_info.nyse[ticker[0]][0])
								self.Sector.append(company_info.nyse[ticker[0]][1])
								self.Industry.append(company_info.nyse[ticker[0]][2])
								
						elif exchange.lower() == "amex":
							if(ticker[0] in company_info.amex.keys()):
								self.Company_Name.append(company_info.amex[ticker[0]][0])
								self.Sector.append(company_info.amex[ticker[0]][1])
								self.Industry.append(company_info.amex[ticker[0]][2])
						else:
							self.Company_Name.append('')
							self.Sector.append('')
							self.Industry.append('')
			except Exception, e:
				print str(e)
			
	def Extract_Headline(self): ## Extracting Headline using regex involving the pattern --> 8/28/2014 5:55:00 PM"|"Head Line"|" 
		try:
			for i in self.ptag:
				self.header.append(i.get_text())
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
				if (self.ticker!=''):
					Utility1 = utility.Utility()
					Utility1.Make_Stock_Dictionary(i, self.dict, self.date)
					self.cmp.append(Utility1.stock_price)
					self.dict={}
				else: 
					self.cmp.append('')
		
		except Exception, e:
			print str(e)

			
	def Extract_Firm(self): # Using |'Firm Name Co.'| expression for extracting firm name
				try:
					for i in self.ptag:
						tokenised = nltk.word_tokenize(i.get_text())
						tagged = nltk.pos_tag(tokenised)
						kgb = []
						for i in tagged:
							if(i[1]=='NNP'):
								kgb.append(i[0])
							else:
								break
						stavka = ''
						for i in kgb:
							stavka += i
							stavka += ' '
						self.firm.append(stavka)
				except Exception, e:
					print str(e)
			

	def MOW(self): # Using self.reco_action and self.reco_type to get reco_action_mow and reco_type_mow
		try:
			for i in self.ptag:
				header = i.get_text()
				body = i.get_text()
				ORIG = orig.Return_ORIG()
				string = "to\s+([A-Za-z]*)"
				string2 = "a\s+([A-Za-z]*)"
				ORIG.rec_type_mow(body)
				reco_type = ORIG.reco_type
				reco_action = re.findall(string,body)
				if(reco_action==[]):
					reco_action = re.findall(string2,body)
				if(reco_action==[]):
					reco_action = ''
				else:
					reco_action = reco_action[0]
				MOW1 = mow.MOW()
				MOW1.rec_act_mow(reco_action)
				reco_action_mow = MOW1.reco_action_mow
				MOW1.rec_type_mow(reco_type)
				reco_type_mow = MOW1.reco_type_mow
				self.reco_action.append(reco_action)
				self.reco_action_mow.append(reco_action_mow)
				self.reco_type.append(reco_type)
				self.reco_type_mow.append(reco_type_mow)
		
		except Exception, e:
			print str(e)
	
	def Csv_file_input(self): ## Every time appending the all the columns extracted from the RSS Feeds into the CSV file.
		try:
			for i in range(0,len(self.ticker)):
				Csv_Data.append([self.date, self.Company_Name[i], self.ticker[i], self.firm[i], self.reco_action[i], \
					self.reco_action_mow[i], self.cmp[i], self.PriceTarget[i], \
					self.horizon, self.analyst_first_name, self.analyst_last_name, \
					self.analyst_email, self.analyst_tc, self.Sector[i], \
					self.Industry[i], self.header[i], self.notes, self.reco_type[i], \
					self.reco_type_mow[i], self.SourceLink, self.status, self.curated, self.raw])
					
			for i in range(0,len(self.ticker)):
				Csv_Data1.append([self.firm[i]])
			
			for i in range(0,len(self.ticker)):
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
		if(not(FParser.Filter_Feeds())):
			continue
		FParser.Clean_Ptags()
		FParser.Extract_Date()
		FParser.Extract_Ticker()
		FParser.Extract_Stock_Price()
		FParser.Extract_SourceLink()
		FParser.Extract_Headline()
		FParser.Extract_TP()
		FParser.Extract_Firm()
		FParser.MOW()
		FParser.Csv_file_input()
		#FParser.Print()
		FParser.file_pointer.close()
	
	
	print 'Finish'
	# Write the csv output
	with open('street_insider.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data)
	
	with open('street_insider1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('street_insider2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)
	
	# Removing Temporary Files
	#os.remove("RecoAction_orig.txt") We Don't access the website to get the data
	
	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))