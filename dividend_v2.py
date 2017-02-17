# -*- coding: utf-8 -*-
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
		self.html = BeautifulSoup(re.findall(r'\"(<html>.*</html>)\"',self.data,re.DOTALL)[0])
		self.html = self.html.decode('unicode-escape').encode('ascii','ignore')
		self.html = self.html.replace("\n","")
		self.html = BeautifulSoup(self.html)
		self.key  = []
		self.value = []
		self.ptag = self.html.findAll('p',{'class':''})
		
	def Filter_Feeds(self): ## Extracting Headline using regex involving the pattern --> 8/28/2014 5:55:00 PM"|"Head Line"|"
		try:
			header = re.findall(r'\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M\"\|\"(.*?)\"\|\"', self.data)
			if "analyst moves:".lower() in header[0].lower():
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
			kgb=[]
			for i in self.ptag:
				kgb.append(str(i))
			flag =0
			for i in kgb:
				#print i
				if flag==0:
					if '<p> <strong>' in i:
						j=	BeautifulSoup(i)
						flag=1
						self.key.append(j) # Beautiful Soup object
						continue
				if flag==1:
					j=	BeautifulSoup(i)
					flag=0
					#print	j.get_text().encode('utf-8')
					self.value.append(j)
				
			#print self.value
			#print self.key
			#print self.ptag
		except Exception, e:
			print str(e)
			
	def Extract_TP(self):
		try:
			#TP(value[1].get_text().encode('utf-8'))
			for i in self.value:
				string = "\$([0-9]*) price target"
				string2 = "price target [A-Za-z]*\s+\$([0-9]*)"
				gamma =  re.findall(string,i.get_text().encode('utf-8'))
				
				if(gamma==[]):
					gamma =  re.findall(string2,i.get_text().encode('utf-8'))
				
				if(gamma ==[]):
					self.PriceTarget.append('')
				else:
					self.PriceTarget.append(gamma[0])	
					
		except Exception, e:
			print str(e)
			
	def Extract_Ticker(self):
			try:
				#ticker =  Ticker(value[0]) 
				#value.strong.get_text()
				for i in self.value:
					if (i.strong!=None):
						ticker = i.strong.get_text().split()[0]
						self.ticker.append(i.strong.get_text().split()[0])
					else:
						self.ticker.append('')
						self.Company_Name.append('')
						self.Industry.append('')
						self.Sector.append('')
						continue 
					
					
					for index in ['amex.csv', 'nyse.csv', 'nasdaq.csv']:
						with open(index, 'r') as csvfile:
							read_csv = csv.reader(csvfile, delimiter = ',')
							for row in read_csv:
								if 	ticker == row[0]:
										#print ticker
									#Company_Name = row[1]
										self.Company_Name.append(row[1])
									#Industry = row[7]
										self.Industry.append(row[7])
									#Sector = row[6]
										self.Sector.append(row[6])
										break		
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
					for i in self.key:
						gamma =	i.get_text().encode('utf-8').split()
						poison = 0;
						meet = 0;
						final = ''

						if 'ed ' in i.get_text().encode('utf-8'):
							poison = 1;
								
						for i in gamma:
								
							if i=='at':
								meet = 1;
								
							elif meet == 0:
								continue
								
							else: 
								final += i
								final += ''

						if meet == 0 and poison==0:
							final = ''
							final = gamma[0]

						self.firm.append(final)
				
				except Exception, e:
					print str(e)
			

	def MOW(self): # Using self.reco_action and self.reco_type to get reco_action_mow and reco_type_mow
		try:
			#MOW(key[0].get_text().encode('utf-8'),value[0].get_text().encode('utf-8'))
			for i in range(0,len(self.value)):
				#print self.value[i]
				ORIG = orig.Return_ORIG()
				string = "to\s+([A-Za-z]*)"
				string2 = "a\s+([A-Za-z]*)"
				ORIG.rec_type_mow(self.value[i].get_text().encode('utf-8'))
				reco_type = ORIG.reco_type
				self.reco_type.append(reco_type)
				reco_action = re.findall(string,self.value[i].get_text().encode('utf-8'))
				#print reco_action
				if(reco_action==[]):
					reco_action = re.findall(string2,self.value[i].get_text().encode('utf-8'))
					#print reco_action
				
				if(reco_action==[]):
					reco_action = ''
				else:
					reco_action = reco_action[0]
					
				self.reco_action.append(reco_action)
					
				MOW1 = mow.MOW()
				MOW1.rec_act_mow(reco_action)
				reco_action_mow = MOW1.reco_action_mow
				#print reco_action_mow
				self.reco_action_mow.append(reco_action_mow)
				
				MOW1.rec_type_mow(reco_type)
				reco_type_mow = MOW1.reco_type_mow
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
		FParser.Extract_Headline()
		FParser.Clean_Ptags()
		FParser.Extract_Date()
		FParser.Extract_Ticker()
		FParser.Extract_Stock_Price()
		FParser.Extract_Firm()
		FParser.Extract_SourceLink()
		FParser.Extract_TP()
		FParser.MOW()
		FParser.Csv_file_input()
		FParser.file_pointer.close()
	
	
	print 'Finish'
	# Write the csv output
	with open('dividend.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data)
	
	with open('dividend1.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data1)
		
	with open('dividend2.csv', 'w') as fp:
		csv_write = csv.writer(fp, delimiter= ',')
		csv_write.writerows(Csv_Data2)

	## Removing the .1 files
	for file_name in os.listdir('.'):
		if re.search('[0-9]*\.[1-2]', file_name):
			os.remove(os.path.join('.', file_name))