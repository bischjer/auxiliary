def as_role(method):
    return method

def as_user(method):
    return method


def expected(actual_result,
             expected_result,
             service=""):
    if actual_result != expected_result:
        color_s = "\033[31m Error: %s \033[0m"
        print color_s % service
    else:
        color_s = "\033[32m OK: %s \033[0m"
        print color_s % service
    
