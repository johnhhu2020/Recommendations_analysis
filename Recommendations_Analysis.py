class Rec_Search:
    '''
    Rec_Search: 
    # Search for successful in app product recommendation

    str_file:
        the file containing user in-app behavior records
        including timestamp, roleid, action, and item id
    processed_file: 
        the expected result is: returning the first Look record between Recommendation and Buy
    '''
    
    
    def __init__(self):
        
        import sys
        self.str_file = sys.argv[1]
        self.processed_file = sys.argv[2]

    
    def search(self):
         with open(self.str_file, "r") as input: 
              with open(self.processed_file, "w") as output: 
                   lines = input.readlines()
                   rn = len(lines)
                   
                   for i in range(1, rn-1, 1):
                       i_line = lines[i]

                       if i_line.split(" ")[3] == "rec":
                           search_p = i_line.split(" ")[4]

                           for j in range(i, rn-1, 1):
                               j_line = lines[j]

                               if j_line.split(" ")[3] == "rec":
                                   j_line = lines[j-1]
                               
                                   if j_line.split(" ")[3] != "rec" and j_line.split(" ")[4] == search_p and j_line.split(" ")[3] == "buy":
                                       for k in range(i, rn-1, 1):
                                           k_line = lines[k]

                                           if k_line.split(" ")[3] == "look":
                                               output.write(k_line + '\n')
                                               break


if __name__ == "__main__":
    Ext = Rec_Search()
    Ext.search()
