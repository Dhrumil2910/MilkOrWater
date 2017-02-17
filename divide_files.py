''' To split the huge input to seperate files
 The input file is having Line carriage ending as raw data set is created \in windows/
 Each rss feed is split into 2 parts, one part containing body html only and another containing all the fields of the 
  extracted rss feeds
 '''
class MakeFiles:
    def __init__(self, filename):
        self.filename = filename
        self.regex =  "|"
        self.regex1 = "From (address)"
        self.mode = 0
        self.integ = 1
        self.index = str(int(self.integ) + 1) + ".1" 
        self.count = 2
        self.count_files = 0

    def divide_into_files(self): # Dividing the file into two parts that is *.1 and *.2 files
        fo = open(self.filename, 'r')            
        for line in fo:
            if self.regex1 in line: # First it will check for unwanted lines in the file, if they exist, function will ignore them
                continue
            else:
    
                if self.regex in line:
    
                    if self.mode == 0: # self.mode is checking whether a particular file is open or close for writing.
                        self.mode = 1
                        fw = open(self.index, 'w')
                        self.count_files += 1 # self.count_files is the sum of the no. of .1 and no of .2 files made
                    elif self.mode == 1:
                        if(self.count%2 != 0):
                            f1.close()
                        fw.close()
                        self.count += 1  # self.count checks whether the current file being written is .1 file or .2 file
                        if self.count%2 == 0:
                            index1 = float(self.index) + 0.9
                            self.index = str(index1)
                            fw = open(self.index,'w')
                            self.count_files += 1
                        else:
                            pre_index = self.index
                            index1 = float(self.index) + 0.1
                            self.index = str(index1)
                            f1 = open(pre_index,'a')
                            fw = open(self.index,'w')
                            self.count_files += 1 

                if self.mode == 1:
                    if self.count%2 == 0:    
                        fw.write(line)
                    else:
                        fw.write(line)
                        f1.write(line)
        fo.close()