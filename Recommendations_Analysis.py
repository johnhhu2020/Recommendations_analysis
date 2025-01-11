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
                  
                  for i in range(0, rn, 1):
                      i_line = lines[i]
                      i_action, i_product = i_line.split(" ")[3], i_line.split(" ")[4]
                      
                      if i_action == "rec":
                          for j in range(i, rn, 1):
                              j_line = lines[j]
                              j_action, j_product = j_line.split(" ")[3], j_line.split(" ")[4]
                              
                              if j_product == i_product and j_action == "buy":
                                  for k in range(i, j, 1):
                                      k_line = lines[k]
                                      k_action, k_product = k_line.split(" ")[3], k_line.split(" ")[4]
                                      
                                      if k_product == j_product and k_action == "look" and \
                                        all (lines[e].split(" ")[3] != "buy" for e in range(i, k, 1)) and \
                                            all (lines[e].split(" ")[3] != "buy" for e in range(k, j, 1)):
                                          output.write(k_line)
                                          break


if __name__ == "__main__":
    Ext = Rec_Search()
    Ext.search()
