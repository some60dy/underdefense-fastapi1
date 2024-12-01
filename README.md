    Додаток має місти наступні ендпоінти:
        1.1 /info - Має виводити інформацію про додаток, вас як автора
        1.2 /get/all - Має виводити CVE за останні 5 днів. Максимум 40 CVE
        1.3 /get/new - Має виводити 10 найновіших CVE
        1.4. /get/known - Має виводити CVE в яких knownRansomwareCampaignUse - Known, максимум 10.
        1.5 /get?query="key" - Має виводити CVE які містять ключове слово

Main files
main.py - the main file containing FastAPI routes and handlers for various requests.
templates/ - a folder with Jinja2 templates for rendering HTML.
static/ - a folder for storing CSS for styles.

Routes.
/ - The main page with information about the application.
/load_vulnerabilities - Loads the list of CVEs.
/get/new - Shows the 10 most recent CVEs.
/get/all - Shows CVEs added in the last 5 days.
/get/known - Shows CVEs that are known.
 /get?query=key - Search for a CVE by query.
 
1. Results

Main page
![image](https://github.com/user-attachments/assets/3816f2e7-9982-4c32-b12d-363507e23431)

Info
![image](https://github.com/user-attachments/assets/c1475fbb-107e-48e0-9717-2612528c8db9)

Newest by ID
![image](https://github.com/user-attachments/assets/b051a63a-9d2e-4fad-a51f-cd54f4d4bd56)

Recent by time
![image](https://github.com/user-attachments/assets/1786af6d-2676-40b6-a5c9-7d5afdfe7b75)

Known
![image](https://github.com/user-attachments/assets/d5b1df41-cfd9-4894-acf4-f8dae36fb567)

get?query=FTP
![image](https://github.com/user-attachments/assets/1f5ec898-b7f9-4ad4-aa2d-c032172daecf)



The given code is a FastAPI application that interacts with the CISA to retrieve and display information about known exploited vulnerabilities. Here's a detailed explanation of each part of the code:

At the beginning, the necessary modules are imported: FastAPI, Query, and Request from FastAPI, which are used for building the web application and handling requests. Jinja2Templates is imported for rendering HTML templates, and StaticFiles is used to serve static files (like CSS, JavaScript, or images). The requests module is used to make HTTP requests to fetch data from an external json.

The app object is created as an instance of FastAPI, which represents the application. Then, a Jinja2Templates object is initialized with the directory "templates", which will be used to store HTML templates. The app.mount("/static", StaticFiles(directory="static"), name="static") line is used to serve static files from the "static" directory, which can be used to include stylesheets, JavaScript, or other media in the web pages.

A global variable url is defined, which stores the URL to the CISA ur; that provides the known exploited vulnerabilities in JSON format. Another global variable, vulnerabilities, is initialized as an empty list. This will hold the list of vulnerabilities fetched from the CISA.

These handlers define different endpoints for the web application:

@app.get("/info") returns a page with information about the application. The info function receives the request parameter, which is passed to the template, along with the application name, author, and description. It uses the TemplateResponse method to render the "info.html" template with the provided data.

@app.get("/") responsible for loading and displaying the vulnerabilities data. Inside the function, an HTTP request is made to the url using the requests.get() function to fetch the JSON data. If the response is successful (status code 200), the vulnerabilities list is populated with the data. If there is an issue parsing the JSON, an error message is returned. Once the data is fetched, it renders the "index.html" template.

@app.get("/get/new")returns the 10 newest CVEs (Common Vulnerabilities and Exposures). The function sorts the vulnerabilities list in descending order based on the cveID and then returns the top 10 results by rendering the "cve_list.html" template.

@app.get("/get/all") returns vulnerabilities from the last 5 days. It first determines the most recent dateAdded from the vulnerabilities list and then filters vulnerabilities that were added within the last 5 days. The results are sorted by the dateAdded field in descending order and passed to the "cve_list.html" template for rendering.

@app.get("/get/known") returns vulnerabilities related to known ransomware campaigns. It filters the vulnerabilities list by checking if the knownRansomwareCampaignUse field is set to "Known". It collects these vulnerabilities and returns the first 10 results by rendering the "cve_list.html" template.

@app.get("/get") allows users to search for vulnerabilities based on a query. The query parameter is taken from the URL using FastAPI's Query class. The function searches through the vulnerabilities list, checking if the cveID or notes fields contain the search term (case-insensitive). It collects matching vulnerabilities and returns the results by rendering the "cve_list.html" template.

Finnally, Im going to sleep.
