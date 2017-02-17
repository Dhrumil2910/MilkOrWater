# CSV File Header
Csv_Data = [["Date", "Company_Name", "TICKER", "FirmName", "RecoAction_orig", "RecoAction_Mow", "CMP"\
, "TP", "Horizon", "Analyst F name", "Analyst L name", "Analyst email", "Analyst tc",\
"Sector", "Industry", "Headline", "notes", "RecoType_orig", "RecoType_Mow", "SourceLink", "Status", "Curated", "Raw"]]

Csv_Data1 = [["FirmName"]]

Csv_Data2 = [["Company_Name", "FirmName"]]


class Backbone:
	def __init__(self):
		self.curated= 3
		self.notes = ""
		self.status = ""
		self.analyst_email = ""
		self.analyst_tc = ""