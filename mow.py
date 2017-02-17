# Instances of Class MOW are used for finding the client's company reco. based on the original reco. in dataset , used in all 3 parsers
class MOW:

    def __init__(self):
        self.reco_action_mow = ""
        self.reco_type_mow = ""

    def rec_act_mow(self, original): # Original is rec_action_orig string
        original = original.lower()
    
        if "positive" in original: # Buy Cases
            self.reco_action_mow = "Buy"
        
        elif "add" in original:
            self.reco_action_mow = "Buy"
        
        elif "accumulate" in original:
            self.reco_action_mow = "Buy"
        
        elif "buy"  in original:
            self.reco_action_mow = "Buy"
            
        elif ("top" or "best") in original and ("pick") in original:
            self.reco_action_mow = "Buy"
            
        elif ("out") in original and ("perform") in original:
            self.reco_action_mow = "Buy"
            
        elif ("over") in original and ("weight") in original:
            self.reco_action_mow = "Buy"
            
        elif ("above") in original and ("average") in original:
            self.reco_action_mow = "Buy"
        
        elif("under") in original and ("weight") in original: # Sell Cases
            self.reco_action_mow = "Sell"
            
        elif("under") in original and ("perform") in original:
            self.reco_action_mow = "Sell"
            
        elif "reduce" in original:
            self.reco_action_mow = "Sell"
            
        elif "sell" in original:
            self.reco_action_mow = "Sell"
                                                        
        elif "hold" in original: # Hold Cases
            self.reco_action_mow = "Hold"
            
        elif "average" in original:
            self.reco_action_mow = "Hold"
            
        elif "perform" in original:
            self.reco_action_mow = "Hold"
            
        elif "neutral" in original:
            self.reco_action_mow = "Hold"
        
        elif("equal") in original and ("weight") in original:
            self.reco_action_mow = "Hold"
            
        elif("in") in original and ("line") in original:
            self.reco_action_mow = "Hold"
            
    def rec_type_mow(self,original):    # Here Original is reco_type_orig string
        original = original.lower()

        
        if "downgrade" in original:
            self.reco_type_mow = "Downgrade"
        
        elif "upgrade" in original:
            self.reco_type_mow = "Upgrade"
        
        elif "reiterate" in original:
            self.reco_type_mow = "Reiterate"
            
        elif "initiate" in original:
            self.reco_type_mow = "Initiate"
        
        elif ("lower" or "cut" or "boost" or "raise" or "moves") in original and "estimate" in original or ("price" and "target") in original:
            self.reco_type_mow = "Revision"
        
        elif "change" in original:
            self.reco_type_mow = "Revision"
		