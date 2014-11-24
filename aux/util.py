from colorama import Fore, Back, Style
import os

def as_role(method):
    return method

def as_user(method):
    return method


def expected(actual_result,
             expected_result,
             service="",
             note=None,
             error_msg=None):

    if actual_result != expected_result:
        # color_s = Fore.RED + "Error: %s" + Fore.RESET
        color_s = "Err: %s"
        print color_s % service
        if note is not None:
            print "   : %s" % (note)
        if error_msg is not None:
            print "   : %s" % (error_msg)
    else:
        # color_s = Fore.GREEN + "OK: %s" + Fore.RESET
        color_s = "OK : %s"
        print color_s % service
        if note is not None:
            print "   : %s" % (note)    
