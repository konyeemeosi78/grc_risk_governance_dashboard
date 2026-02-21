import csv
from ingestion import fetch_cve_data
from risk_engine import evaluate_risk

def load_control_mappings():
    """
    Load COBIT to NIST control mappings from CSV.
    """
    mappings = []
    with open("controls.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mappings.append(row)
    return mappings


def integrate_risk_data():
    """
    Integrate governance controls with public risk data
    and evaluate risk levels.
    """
    cve_data = fetch_cve_data()
    control_mappings = load_control_mappings()

    integrated_results = []

    for item in cve_data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        metrics = cve.get("metrics", {})

        # Extract CVSS base score if available
        cvss_score = None

        if "cvssMetricV31" in metrics:
             cvss_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV30" in metrics:
            cvss_score = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV2" in metrics:
            cvss_score = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
        if cvss_score is None:
              continue



        risk_level = evaluate_risk(cvss_score)

        integrated_results.append({
            "cve_id": cve.get("id"),
            "cvss_score": cvss_score,
            "risk_level": risk_level,
            "applicable_controls": control_mappings
        })

    return integrated_results
