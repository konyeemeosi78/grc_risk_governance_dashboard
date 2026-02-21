def evaluate_risk(cvss_score):
    """
    Evaluate risk level based on CVSS score.
    This function represents the Risk Evaluation Engine.
    """

    if cvss_score >= 9.0:
        return "High"
    elif cvss_score >= 7.0:
        return "Medium"
    else:
        return "Low"
