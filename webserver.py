import os
import json
import requests
from flask import Flask, request, abort

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/nenenen/refs/heads/main/cousins.json"

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")
    
    # Fetch fresh data every request
    try:
        r = requests.get(JSON_URL)
        cousins = r.json()
    except:
        cousins = {}

    data = cousins.get(user_id)
    if not data or data.get("token") != token:
        return abort(403)

    html = f"""
    <html>
    <head><title>{data['name']}'s Profile</title></head>
    <body>
        <h1>{data['name']}'s Cousin Profile</h1>
        <p>Reputation: {data['rep']}/100</p>
        <p>Rank: #{data['rank']}</p>
        <p>Cousin ID: {data['cousin_id']}</p>
        {'<img src="'+data['banner']+'">' if data.get('banner') else ''}
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
