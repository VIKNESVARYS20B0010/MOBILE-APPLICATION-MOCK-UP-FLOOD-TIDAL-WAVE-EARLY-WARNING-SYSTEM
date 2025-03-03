from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_flood_data():
    url = "https://publicinfobanjir.water.gov.my/?lang=en"  # Public InfoBanjir URL
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents bot detection
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to retrieve data"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract flood data (Modify selectors based on website structure)
    flood_events = []
    flood_table = soup.find("table", {"id": "floodTable"})  # Example, change as needed
    if flood_table:
        for row in flood_table.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            if len(cols) >= 4:
                flood_events.append({
                    "location": cols[0].text.strip(),
                    "latitude": float(cols[1].text.strip()),
                    "longitude": float(cols[2].text.strip()),
                    "severity": cols[3].text.strip()
                })
    
    return flood_events

@app.route("/api/floods", methods=["GET"])
def get_flood_data():
    return jsonify(scrape_flood_data())

if __name__ == "__main__":
    app.run(debug=True)
