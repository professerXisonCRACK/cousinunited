import os
import json
from flask import Flask, request, abort

app = Flask(__name__)
DATA_FILE = "cousins.json"

def load_cousins():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")
    
    cousins = load_cousins()  # load fresh every time
    data = cousins.get(user_id)
    if not data or data.get("token") != token:
        return abort(403)

    html = f"""
    <html>
    <head>
        <title>{data['name']}'s Profile</title>
        <style>
            body {{
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background: #1f1f1f;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                text-align: center;
                width: 350px;
            }}
            .card img {{
                border-radius: 10px;
                max-width: 100%;
                margin-top: 15px;
            }}
            h1 {{
                color: #f5a623;
            }}
            p {{
                font-size: 16px;
                margin: 8px 0;
            }}
            .rep {{
                color: #4caf50;
                font-weight: bold;
            }}
            .rank {{
                color: #2196f3;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{data['name']}</h1>
            <p>Reputation: <span class="rep">{data['rep']}/100</span></p>
            <p>Rank: <span class="rank">#{data['rank']}</span></p>
            <p>Cousin ID: {data['cousin_id']}</p>
            {'<img src="'+data['banner']+'" alt="Banner">' if data.get('banner') else ''}
        </div>
    </body>
    </html>
    """
    return html

@app.route("/")
def index():
    return "Cousin profile webserver is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
