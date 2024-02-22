import sys 

BATCH_NAME = "Python Class"


def get_supported_functions(input_object):
    """
    This will show all the functions apart from 
    the built-ins for a particular object
    """

    functions = []

    for function_name in dir(input_object):
        if not ("_" in function_name):
            functions.append(function_name)

    return functions



def get_sys_path():
    sys_path = None

    for path in sys.path:
        if "site-packages" in path:
            print(path)
            sys_path = path 
            break

    return sys_path


def get_team_members():
    return ["firoz", "karthik", "betrand", "santhosh"]
