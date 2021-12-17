def scadaActualPoint(stateName: str):
    """
    Args:
        stateName (str): sem state code for graph plotting
    Returns:
        Name of the state for graph plotting!!!
    """
    if stateName == "GU":
        return "WRLDCMP.SCADA1.A0043301"
    elif stateName == "MP":
        return "WRLDCMP.SCADA1.A0043339"
    elif stateName == "MH":
        return "WRLDCMP.SCADA1.A0043342"
    elif stateName == "DNH":
        return "WRLDCMP.SCADA1.A0043290"
    elif stateName == "DD":
        return "WRLDCMP.SCADA1.A0043282"
    elif stateName == "GO":
        return "WRLDCMP.SCADA1.A0043304"
    elif stateName == "CS":
        return "WRLDCMP.SCADA1.A0043277"