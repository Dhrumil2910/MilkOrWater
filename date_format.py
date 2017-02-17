''' Used to convert the date given on http://www.benzinga.com/stock/<TICKER>/ratings to the format which can be compared 
 with those in benzinga rss feeds''' 
import re
class convert_date:
    def __init__(self, date):
        self.date = date
        self.dict = {"Jan":"1", "Feb":"2", "Mar":"3", "Apr":"4", "May":"5", "Jun":"6", "Jul":"7", "Aug":"8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12"}
        self.final = ""
    def convert_into_a_specific_format(self): # Function for date conversion
        date_splited = self.date.split() # splitting the date of the format like "Oct 3 2014"
        date_month_index = self.dict[date_splited[0]] # then selecting the month index from the above defined dictionary.
        length = len(date_splited[1])
        date_day = date_splited[1][:length-1] # inserting the year and day into temporary variables
        date_year = date_splited[2]
        full_date = date_month_index + "/" + date_day + "/" + date_year #appending all the defined variables to get date into format "03/10/2014"
        self.final = full_date




