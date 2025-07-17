import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    #this info will probably give you all the information like on which file the exception has occurred,
    #on which line number, the exception has occurred.
    #all those information will be probably given and will be stored in this particular variable 

    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    
# I've created a function over here which will probably give you a message like how your message should
# look like inside your file with respect to your custom exception.

# And then we created our own custom exception class, which is inheriting from exception.

# we have also overridden the init method right over here, and I've created an error message variable
# inside this.

# And finally when we print this right when we raise the custom exception, in short, when we print it,
# it is going to print the error message itself.

# So this is with respect to the exception handling.




    

        #this info will probably give you all the information like on which file the exception has occurred,
    #on which line number, the exception has occurred.
    #All those information will be probably given and will be stored in this particular variable 