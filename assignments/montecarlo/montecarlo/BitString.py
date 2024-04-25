import numpy as np
import math             



class BitString:
    """
    Simple class to implement a config of bits
    """
    def __init__(self, N):
        """
        Defines the number of binary digits that the BitString will have
        """
        self.N = N
        self.config = np.zeros(N, dtype=int) 

    def __repr__(self):
        #Creating an empty string to add the array self.config to
        str1 = ""

        #for loop to add a string version of each entry from the array to the string
        for entry in self.config:
            str1 += str(entry)

        #section of method to define the new string
        return str1

    def __eq__(self, other): 
        str_sel = ""
        str_oth = ""
        for entry in self.config: #for loop to convert arrays to strings
            str_sel += str(entry)
        for entry in other.config:
            str_oth +=str(entry)

        if str_sel == str_oth: #compare the strings
            return True #defining the bolean value of equivalance here
        return False
    
    def __len__(self):
        #needed to establish the return value to be the len() of self.config
        return len(self.config)

    def on(self):
        """
        Returns the number of binary digits that are 1
        """
        #make a variable to save the number of 1's
        on_bit = 0
        for i in range(len(self.config)): # for loop to to increase on_count for each entry = 1
            if self.config[i] == 1:
                on_bit += 1
        #need to return for the function to actually do something
        return on_bit

    def off(self):
        """
        Returns the number of binary digits that are 0
        """
        #make a variable to save the number of 0's
        off_bit = 0
        for i in range(len(self.config)): # for loop to to increase off_count for each entry = 1
            if self.config[i] == 0:
                off_bit += 1
        return off_bit
    
    def flip_site(self,i):
        """
        Converts the specified digit of the bitstring from 0 to 1 or 1 to 0
        """
        #create a for loop to switch the designated entry
        # if the ith entry of array is 0, set ith entry to 1
        if self.config[i] == 0:
            self.config[i] = 1
        #else set entry to 0
        else:
            self.config[i] = 0
    
    def int(self): #converts bindary to decimal
        """
        Changes the bitstring to a decimal base number
        """
        count = 0
        int_bit = 0

        for i in range(len(self.config), 0, -1): #for loop to add 2^count of each binary digit
            int_bit += (int(self.config[i-1]) * (2**count)) 
            count += 1

            if count > len(self.config): #saftey loop
                return "loop error :("
        
        return int_bit
 

    def set_config(self, s:list[int]):
        """
        Change the current bitstring to the inputed bistring configuration
        """
        self.config = s
        
    def set_int_config(self, dec:int):
        """
        Change the current bitstring to the inputed decimal configuration
        """
        str_len = len(self.config) #save length of bit array
        self.config = np.zeros(str_len, dtype=int) #set bit array to zero

        dec_int = dec #track variable division and act as while loop counter
        dec_rem = 0
        count = 0 #counter in while loop to determine string position

        while dec_int != 0:
            dec_rem = dec_int % 2 # get remainder of decimal number, convert to bin w/if else
            if dec_rem == 1: #if-else to add numbers to end of string
                self.config[str_len - count -1] = 1
            else:
                self.config[str_len - count -1] = 0

            count += 1
            dec_int = dec_int // 2 #division at end of loop to help end early 
            #eventually will go to the value zero
        
