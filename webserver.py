import os
from flask import Flask, request, abort
import json

app = Flask(__name__)
DATA_FILE = "cousins.json"

# Auto-create file if missing (won't overwrite existing data)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        f.write("{}")

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")
    
    # Load fresh data every time
    with open(DATA_FILE) as f:
        cousins = json.load(f)
    
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
