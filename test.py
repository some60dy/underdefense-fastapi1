from fastapi import FastAPI, Query
from datetime import datetime, timedelta
import requests

app = FastAPI()

# Global Variables
JSON_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DATA = []

# Load JSON Data on Startup
@app.on_event("startup")
async def load_data():
    global DATA
    response = requests.get(JSON_URL)
    if response.status_code == 200:
        try:
            DATA = response.json().get("vulnerabilities", [])
        except Exception as e:
            print(f"Error parsing JSON: {e}")
    else:
        print("Failed to fetch data from the URL.")

@app.get("/info")
async def app_info():
    return {
        "app_name": "FastAPI CVE Viewer",
        "author": "Taras Popovych",
        "description": "An application to view CVE data."
    }

@app.get("/get/all")
async def get_recent_cves():
    """Fetch CVEs added in the last 5 days relative to the newest date in the dataset."""
    if not DATA:
        return []

    # Find the most recent date in the dataset
    newest_date = max(
        datetime.strptime(cve["dateAdded"], "%Y-%m-%d") for cve in DATA if "dateAdded" in cve
    )

    cutoff_date = newest_date - timedelta(days=5)

    # Filter CVEs within the last 5 days
    filtered_cves = [
        cve for cve in DATA
        if "dateAdded" in cve and datetime.strptime(cve["dateAdded"], "%Y-%m-%d") >= cutoff_date
    ]
    return filtered_cves[:40]

@app.get("/get/new")
async def get_new_cves():
    """Fetch the 10 newest CVEs based on date added."""
    sorted_cves = sorted(
        DATA, key=lambda x: datetime.strptime(x.get("dateAdded", "1970-01-01"), "%Y-%m-%d"), reverse=True
    )
    return sorted_cves[:10]

@app.get("/get/known")
async def get_known_ransomware():
    """Fetch up to 10 CVEs with 'knownRansomwareCampaignUse': 'Known'."""
    known_ransomware = [
        cve for cve in DATA if cve.get("knownRansomwareCampaignUse", "").lower() == "known"
    ]
    return known_ransomware[:10]

@app.get("/get")
async def search_cves(query: str = Query(...)):
    """Search for CVEs by a query keyword."""
    matching_cves = [
        cve for cve in DATA
        if query.lower() in cve.get("cveID", "").lower() or query.lower() in cve.get("notes", "").lower()
    ]
    return matching_cves
