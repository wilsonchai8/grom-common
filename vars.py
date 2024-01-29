import cProfile

__variables = {}

def var_init():
    global __variables
    __variables = {
        'profile': cProfile.Profile()
    } 
    
def get_vars():
    return __variables