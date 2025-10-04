import os
from flask import Flask, request, abort
import json

app = Flask(__name__)
DATA_FILE = "cousins.json"

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")

    # Load fresh data every time
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            cousins = json.load(f)
    else:
        cousins = {}

    data = cousins.get(user_id)
    if not data or data.get("token") != token:
        return abort(403)  # Forbidden if token is missing/invalid

    # Build the profile HTML
    html = f"""
    <html>
    <head>
        <title>{data['name']}'s Cousin Profile</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #1e1e1e; color: #f0f0f0; }}
            .profile {{ max-width: 600px; margin: 50px auto; padding: 20px; background: #2a2a2a; border-radius: 12px; }}
            img {{ max-width: 100%; border-radius: 8px; }}
            h1 {{ color: #ffcc00; }}
        </style>
    </head>
    <body>
        <div class="profile">
            <h1>{data['name']}'s Cousin Profile</h1>
            <p><strong>Reputation:</strong> {data['rep']}/100</p>
            <p><strong>Rank:</strong> #{data['rank']}</p>
            <p><strong>Cousin ID:</strong> {data['cousin_id']}</p>
            {'<img src="'+data['banner']+'">' if data.get('banner') else ''}
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
