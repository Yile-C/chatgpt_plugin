from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Airtable configuration
AIRTABLE_API_URL = "https://api.airtable.com/v0/appHteagZvsaN3iJT/ESCAP%20Care%20Dataset"
AIRTABLE_API_KEY = "pat9LupkTRizgDI1S.bf542c6adc45ce1c98b4a94f4d8785c71eef0e02d5f2c218719a6d3cf163b7e3"

@app.route("/retrieve", methods=["GET"])
def retrieve():
    # Get the query parameter from the user
    query = request.args.get("query", "").lower()
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

    # Fetch data from Airtable
    response = requests.get(AIRTABLE_API_URL, headers=headers)
    data = response.json()

    # Find records that match the query
    results = []
    for record in data.get("records", []):
        fields = record.get("fields", {})
        # Concatenate all parts of the Full Document Text
        full_text = (
            fields.get("Full Document Text", "") +
            fields.get("Full Document Text (Part 2)", "") +
            fields.get("Full Document Text (Part 3)", "") +
            fields.get("Full Document Text (Part 4)", "")
        ).lower()

        # Check if the query exists in the concatenated text
        if query in full_text:
            results.append({
                "Title": fields.get("Title", ""),
                "Summary": fields.get("Summary", ""),
                "Link": fields.get("Link", ""),
                "Full Document Text": full_text
            })

    if not results:
        return jsonify({"message": "No matching documents found."}), 404

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
@app.route("/.well-known/openapi.json", methods=["GET"])
def serve_openapi_spec():
    return app.send_static_file("openapi.json")
