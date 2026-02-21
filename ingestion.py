import requests

def fetch_cve_data():
    """
    Fetch recent CVE data from the NVD public API.
    This function represents the Data Ingestion Layer.
    """
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch CVE data")

    return response.json()
