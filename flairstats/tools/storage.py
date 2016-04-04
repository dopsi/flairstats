def dictvar(dictionnary, key, var, default):
    """Modify value of dictionnary[key] with var, otherwise set it to default"""
    try:
        dictionnary[key] += var
    except KeyError:
        dictionnary[key] = default
