from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
vulnerabilities = []

@app.get("/info")
def info(request: Request):
    return templates.TemplateResponse("info.html", {
        "request": request,
        "app_name": "CVE Viewer",
        "author": "Taras Popovych",
        "description": "UNDERDEFENSE TASK1"
    })

@app.get("/")
def index(request: Request):
    """Main page with information about CVEs."""
    # load CVE data
    global vulnerabilities
    response = requests.get(url)
    if response.status_code == 200:
        try:
            vulnerabilities = response.json().get("vulnerabilities", [])
        except:
            return {"error": "Could not parse JSON"}
    else:
        return {"error": f"Could not download data, status_code: {response.status_code}"}

    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get/new")
def get_new_cves(request: Request):
    """10 newest CVEs based on the CVE ID."""
    sorted_cves = sorted(vulnerabilities, key=lambda x: x.get("cveID", ""), reverse=True)
    return templates.TemplateResponse("cve_list.html", {"request": request, "cves": sorted_cves[:10]})

@app.get("/get/all")
def get_recent_cves(request: Request):
    """Return CVEs from the last 5 days."""
    recent_cves = []
    max_date = max(vuln["dateAdded"][:10] for vuln in vulnerabilities if "dateAdded" in vuln)
    year, month, day = map(int, max_date.split("-"))
    five_days_ago = f"{year:04d}-{month:02d}-{day - 5:02d}"

    for vuln in vulnerabilities:
        date_added = vuln.get("dateAdded", "")[:10]
        if date_added >= five_days_ago:
            recent_cves.append(vuln)
    
    recent_cves.sort(key=lambda x: x["dateAdded"], reverse=True)
    return templates.TemplateResponse("cve_list.html", {"request": request, "cves": recent_cves[:40]})

@app.get("/get/known")
def get_known_ransomware(request: Request):
    """Return CVEs with known ransomware campaigns."""
    known_ransomware = []
    for vuln in vulnerabilities:
        if vuln.get("knownRansomwareCampaignUse") == "Known":
            known_ransomware.append(vuln)
        if len(known_ransomware) >= 10:
            break
    return templates.TemplateResponse("cve_list.html", {"request": request, "cves": known_ransomware})

@app.get("/get")
def search(request: Request, query: str = Query(...)):
    """Search CVEs based on the query."""
    results = []
    for vuln in vulnerabilities:
        cve_id = vuln.get("cveID", "").lower()
        notes = vuln.get("notes", "").lower()
        if query.lower() in cve_id or query.lower() in notes:
            results.append(vuln)
    return templates.TemplateResponse("cve_list.html", {"request": request, "cves": results})
