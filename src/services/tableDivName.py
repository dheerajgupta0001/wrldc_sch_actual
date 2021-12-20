def tableDivNameRet(stateName: str):
    """
    Args:
        stateName (str): sem state code for graph plotting
    Returns:
        Name of the state for graph plotting!!!
    """
    if stateName == "GU":
        return "GU1"
    elif stateName == "DD":
        return "DD1"
    elif stateName == "GO":
        return "GO1"
    elif stateName == "CS":
        return "CS1"
    elif stateName == "MP":
        return "MP1"
    elif stateName == "MH":
        return "MH1"
    elif stateName == "DNH":
        return "DNH1"