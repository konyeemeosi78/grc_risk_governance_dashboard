Implementation Guide: Integrated GRC Risk Governance Dashboard

Purpose of this Guide
This guide provides a step-by-step walkthrough to reproduce the Chapter 4 artefact locally. It assumes no prior experience and explains what each file does, how to run the system, and how to interpret key code sections.
A. Prerequisites
•	Python installed (recommended: Python 3.11+).
•	Visual Studio Code installed.
•	Internet access (for NVD API calls).
B. Project Setup
B1. Create project folder and open in VS Code
1.	Create a folder named: grc-risk-dashboard
2.	Open VS Code, choose File -> Open Folder, and select grc-risk-dashboard.
B2. Create and activate a Python virtual environment
In VS Code Terminal:
python -m venv venv
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

Reason: a virtual environment isolates dependencies and improves reproducibility.
B3. Install dependencies
pip install pandas requests streamlit pyyaml matplotlib
Reason: these libraries support data ingestion, processing, and visualisation.
C. Project Structure
grc-risk-dashboard/
  app.py
  config.yaml
  controls.csv
  ingestion.py
  risk_engine.py
  integration.py
  data/
    sample_cve.json
  .vscode/
    settings.json
  venv/

Important: only editor configuration should be inside .vscode. All Python files must remain in the project root to allow imports.
D. File-by-file Explanation and Code Walkthrough
D1. config.yaml (Governance Configuration)
Role: stores governance intent (COBIT objectives) and risk appetite thresholds in structured form.
governance:
  framework: COBIT
  objectives:
    - EDM03
    - APO12
    - DSS05

risk_appetite:
  high: unacceptable
  medium: tolerable
  low: acceptable

•	governance.objectives: the governance focus areas the dashboard is aligned to.
•	risk_appetite: a governance framing used to interpret risk levels during review (human decision-makers remain accountable).
D2. controls.csv (Control Mapping Engine)
Role: maps COBIT objectives to NIST SP 800-53 control identifiers. This mapping is defined by humans, not inferred by the system.
cobit_objective,nist_control,description
EDM03,RA-3,Risk Assessment
APO12,RA-5,Vulnerability Scanning
DSS05,SI-2,Flaw Remediation

•	cobit_objective: strategic governance objective.
•	nist_control: operational control identifier.
•	description: plain-language meaning for explainability.
D3. ingestion.py (Data Ingestion Layer)
Role: retrieves public vulnerability intelligence from the NVD CVE API and returns parsed JSON.
import requests

def fetch_cve_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch CVE data")
    return response.json()

•	resultsPerPage=5: limits output for demo stability; increase for more records.
•	status_code check: fails fast if the API is unreachable.
•	response.json(): converts the API response into a Python dictionary.
D4. risk_engine.py (Risk Evaluation Engine)
Role: converts CVSS base scores into governance-friendly risk levels using transparent rules.
def evaluate_risk(cvss_score):
    if cvss_score >= 9.0:
        return "High"
    elif cvss_score >= 7.0:
        return "Medium"
    else:
        return "Low"

•	High: CVSS >= 9.0 (typically critical severity).
•	Medium: 7.0 <= CVSS < 9.0.
•	Low: CVSS < 7.0.
•	Rationale: rule-based scoring is explainable and suitable for governance oversight.
D5. integration.py (Integration Layer)
Role: orchestrates the end-to-end pipeline. It loads control mappings, fetches CVE data, extracts CVSS scores across versions, evaluates risk, and produces an integrated risk register for the dashboard.
import csv
from ingestion import fetch_cve_data
from risk_engine import evaluate_risk

def load_control_mappings():
    mappings = []
    with open("controls.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mappings.append(row)
    return mappings

def integrate_risk_data():
    cve_data = fetch_cve_data()
    control_mappings = load_control_mappings()
    integrated_results = []
    for item in cve_data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        metrics = cve.get("metrics", {})
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

•	load_control_mappings(): reads controls.csv to preserve human-defined governance mapping.
•	fetch_cve_data(): obtains public risk intelligence; this does not influence governance intent.
•	CVSS extraction: supports CVSS v3.1, v3.0, and v2 to accommodate heterogeneous NVD records.
•	evaluate_risk(): converts severity into governance-friendly categories.
•	integrated_results: structured output used by the dashboard and later evaluation.
D6. app.py (Integration and Visualisation Layer)
Role: renders governance-oriented insights using Streamlit. It loads integrated results, shows risk counts, displays a distribution chart, and presents a risk register table.
import streamlit as st
from integration import integrate_risk_data
import pandas as pd

results = integrate_risk_data()
df = pd.DataFrame(results)

chart_type = st.selectbox(
    "Select Risk Distribution View",
    ["Bar Chart", "Pie Chart"]
)

risk_counts = df["risk_level"].value_counts()
if chart_type == "Bar Chart":
    st.bar_chart(risk_counts)
else:
    st.pyplot(risk_counts.plot.pie(autopct="%1.1f%%", ylabel="").figure)

•	selectbox: provides basic interactivity to change the chart type (governance-friendly flexibility).
•	bar chart / pie chart: alternative views over the same aggregated distribution.
•	dataframe table: supports transparency and traceability (CVE ID, score, risk level).
E. Running the Dashboard
3.	Ensure the virtual environment is active (look for (venv) in the terminal).
4.	From the project root, run: streamlit run app.py
5.	Open the browser tab launched by Streamlit.
6.	Use the dropdown to switch bar vs pie chart views.
F. Troubleshooting Notes
•	If changes do not appear: stop Streamlit with CTRL + C and re-run.
•	If imports fail: confirm you are in the project root and Python files are not inside .vscode.
•	If pie chart fails: install matplotlib (pip install matplotlib).
•	If results return zero: restart the Python interpreter to avoid stale imports and confirm NVD results include CVSS metrics.
G. Artefacts to Capture for Chapter 5
•	Dashboard screenshot (overview with metrics).
•	Risk distribution visual (bar and/or pie).
•	Risk register table screenshot.
•	A short log of implementation steps and key design decisions.
