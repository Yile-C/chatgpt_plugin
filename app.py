from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Airtable configuration
AIRTABLE_API_URL = "https://api.airtable.com/v0/appHteagZvsaN3iJT/ESCAP%20Care%20Dataset"
AIRTABLE_API_KEY = "pat9LupkTRizgDI1S.bf542c6adc45ce1c98b4a94f4d8785c71eef0e02d5f2c218719a6d3cf163b7e3"

@app.route("/search", methods=["GET"])
def search():
    # Get the query parameter from the user
    query = request.args.get("query", "").lower()
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    
    # Fetch data from Airtable
    response = requests.get(AIRTABLE_API_URL, headers=headers)
    data = response.json()
    
    # Filter results based on the search query
    results = [
        record for record in data.get("records", [])
        if query in record.get("fields", {}).get("Full Document Text", "").lower()
    ]
    
    # Return the filtered results
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
