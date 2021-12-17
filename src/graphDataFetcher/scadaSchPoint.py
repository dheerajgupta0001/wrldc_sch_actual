def scadaSchPoint(stateName: str):
    """
    Args:
        stateName (str): sem state code for graph plotting
    Returns:
        Name of the state for graph plotting!!!
    """
    if stateName == "GU":
        return "WRLDCMP.SCADA1.A0042247"
    elif stateName == "DD":
        return "WRLDCMP.SCADA1.A0042093"
    elif stateName == "GO":
        return "WRLDCMP.SCADA1.A0042229"
    elif stateName == "CS":
        return "WRLDCMP.SCADA1.A0042066"
    elif stateName == "MP":
        return "WRLDCMP.SCADA1.A0042494"
    elif stateName == "MH":
        return "WRLDCMP.SCADA1.A0042526"
    elif stateName == "DNH":
        return "WRLDCMP.SCADA1.A0042119"