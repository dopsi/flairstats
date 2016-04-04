def dictvar(dictionnary, key, var, default):
    """Modify value of dictionnary[key] with var, otherwise set it to default"""
    try:
        dictionnary[key] += var
    except KeyError:
        dictionnary[key] = default

def dict_check_key(dictionnary, key, default):
    """Check if dictionnary has key, if not set it to default"""
    if key not in dictionnary:
        dictionnary[key] = default
