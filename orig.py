#Used in GainersToday.com parser for finding the original recommendations
class Return_ORIG:

    def __init__(self):
        self.reco_action = ""
        self.reco_type = ""

    def rec_act_mow(self, original): # Original is rss feed headline string
        original = original.lower()
    
        if "positive" in original: # Buy Cases
            self.reco_action = "Positive"
        
        elif "add" in original:
            self.reco_action = "Add"
        
        elif "accumulate" in original:
            self.reco_action = "Accumulate"
        
        elif "buy"  in original:
            self.reco_action = "Buy"
            
        elif ("top" or "best") in original and ("pick") in original:
            self.reco_action = "Top Pick"
            
        elif ("out") in original and ("perform") in original:
            self.reco_action = "Out Perform"
            
        elif ("over") in original and ("weight") in original:
            self.reco_action = "Over Weight"
            
        elif ("above") in original and ("average") in original:
            self.reco_action = "Above Average"
        
        elif("under") in original and ("weight") in original: # Sell Cases
            self.reco_action = "Under Weight"
            
        elif("under") in original and ("perform") in original:
            self.reco_action = "Under Perform"
                 
        elif "reduce" in original:
            self.reco_action = "Reduce"
            
        elif "sell" in original:
            self.reco_action = "Sell"
                                                        
        elif "hold" in original: # Hold Cases
            self.reco_action = "Hold"
            
        elif "average" in original:
            self.reco_action = "Average"
            
        elif "perform" in original:
            self.reco_action = "Perform"
            
        elif "neutral" in original:
            self.reco_action = "Neutral"
        
        elif("equal") in original and ("weight") in original:
            self.reco_action = "Equal Weight"
            
        elif("in") in original  and ("line") in original:
            self.reco_action = "In Line"            
            
    def rec_type_mow(self,original):    # Here Original is rss feed headline string
        original = original.lower()
        
        if "downgrade" in original:
            self.reco_type = "Downgrade"
        
        elif "upgrade" in original:
            self.reco_type = "Upgrade"
        
        elif "reiterate" in original:
            self.reco_type = "Reiterate"
            
        elif "initiate" in original:
            self.reco_type = "Initiate"
        
        elif 'lower' in original and 'estimate' in original:
            self.reco_type = 'Lower Estimate'
		
        elif 'cut' in original and 'estimate' in original:
            self.reco_type = 'Estimate Cut'
			
        elif 'boost' in original and 'estimate' in original:
            self.reco_type = 'Boost Estimate'
		
        elif 'raise' in original and 'estimate' in original:
            self.reco_type = 'Raise Estimate'
		
        elif 'lower' in original and ("price" and "target")  in original:
			self.reco_type = 'Price Target Lowered'
		
        elif 'cut' in original  and ("price" and "target") in original:
            self.reco_type = 'Price Target Cut'
		
        elif 'boost' in original and ("price" and "target") in original:
            self.reco_type = 'Price Target Boosted'
		
        elif 'raise' in original and ("price" and "target") in original:
            self.reco_type = 'Price Target Raised'
		
        elif 'lift' in original and ("price" and "target") in original:
            self.reco_type = 'Price Target Raised'
		
        elif 'move' in original and ("price" and "target") in original:
            self.reco_type = 'Price Target Changed'